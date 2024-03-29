
TAG    			:= $$(git describe --long)
REGISTRY		:= registry.nersc.gov
PROJECT 		:= als
REGISTRY_NAME	:= ${REGISTRY}/${PROJECT}/${IMG}

NAME_WEB_SVC  	:= splash_userservice
IMG_WEB_SVC    		:= ${NAME_WEB_SVC}:${TAG}
REGISTRY_WEB_SVC	:= ${REGISTRY}/${PROJECT}/${NAME_WEB_SVC}:${TAG}

NAME_POLLER		:= splash_ingest_poller
IMG_POLLER   	:= ${NAME_POLLER}:${TAG}
REGISTRY_POLLER	:= ${REGISTRY}/${PROJECT}/${NAME_POLLER}:${TAG}

.PHONY: build

hello:
	@echo "Hello" ${REGISTRY}

build_service:
	@docker build -t ${IMG_WEB_SVC} -f Dockerfile .
	@echo "tagging to: " ${IMG_WEB_SVC}    ${REGISTRY_WEB_SVC}
	@docker tag ${IMG_WEB_SVC} ${REGISTRY_WEB_SVC}
 
push_service:
	@echo "Pushing " ${REGISTRY_WEB_SVC}
	@docker push ${REGISTRY_WEB_SVC}
