app.controller("crawlcontroller", function($http, $scope,$resource,$uibModal,Notification){
	$scope.initialise = function(){
		$scope.crawls = []
		$scope.crawls_resource = $resource("api/crawls/:id")
		$scope.images_resource = $resource("api/images/:id")
		$scope.page=1
		$scope.images_page = 1
		$scope.crawl_result = $scope.crawls_resource.get({'page' : $scope.page}).$promise.then(function(data) {
		   $scope.crawls['items'] = data.results
		   $scope.crawls['next'] = data.next
		   $scope.selected_crawl = {"id" : $scope.crawls['items'][0]['id']}
	       $scope.selected_crawl['images'] = $scope.images_resource.get({"crawl" : $scope.selected_crawl.id,'page' : $scope.images_page})
	   });
	}
	$scope.crawl_changed = function(crawl_id) {
		$scope.images_page = 1
		$scope.selected_crawl.id = crawl_id
		$scope.selected_crawl.images = $scope.images_resource.get({"crawl" : $scope.selected_crawl.id})
	}

	var createCrawlController = function ($scope,$uibModalInstance) {
    $scope.crawlParams = {}
    $scope.submitForm = function () {
        if ($scope.form.userForm.$valid) {
            console.log('user form is in scope');
            $modalInstance.close('closed');
        } else {
            console.log('userform is not in scope');
        }
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
	    };

	$scope.ok = function (crawlForm) {
		$scope.submitted = true
		if (crawlForm.$valid != true) {
			return false
		}	
        $uibModalInstance.close($scope.crawlParams);
	};
	};

	$scope.startCrawl = function () {
	   $modalInstance = $uibModal.open({
	   animation: true,
	   templateUrl: '/static/views/startCrawl.html',
	   controller : createCrawlController,
	   size: ''
	 });
	 $modalInstance.result.then(function(result) {
	 		k = Notification.info({message: 'Crawling in progress.Do not close..', positionY: 'bottom', positionX: 'right',delay:""})
            var save_instance = $scope.crawls_resource.save({"url": result.url,"status" : "Started"}).$promise.then(function(data) {
            k.$$state.value.kill()
            Notification.success({message: 'Crawl completed', positionY: 'bottom', positionX: 'right'})
            })
        }, function() {});
	}
	$scope.load_next_crawls = function(){
		if ($scope.crawls['next']) {
		$scope.page+=1
		$scope.crawls_resource.get({'page' : $scope.page}).$promise.then(function(data) {
		   $scope.crawls['items'] = $scope.crawls['items'].concat(data.results)
		   $scope.crawls['next'] = data.next
	   });
	}
	}

	$scope.load_next_images = function() {
		if ($scope.selected_crawl['images'].next) {
		$scope.images_page+=1
		var response = $scope.images_resource.get({"crawl" : $scope.selected_crawl.id,'page' : $scope.images_page})
		$scope.selected_crawl['images'].next = response.next
	}
	}

	$scope.delete_crawl = function(id,index){
		$scope.crawls_resource.delete({ 'id':id }).$promise.then(function(data) {
			$scope.crawls['items'].splice(index, 1)
			Notification.success({message: 'Deleted Successfully', positionY: 'bottom', positionX: 'right'})
		})
	}
	
	$scope.initialise()
})