USERNAME = stanlee321
TARGET_VERSION = v1.0

build:
	# Build the container on your local machine
	docker build -t ${USERNAME}/captcha-ocr-ultra:latest .
up:
	docker run -p 8000:8000 -d ${USERNAME}/captcha-ocr-ultra:latest

tag: 
	docker tag ${USERNAME}/captcha-ocr-ultra:latest ${USERNAME}/captcha-ocr-ultra:${TARGET_VERSION}

push:
	docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}
	docker push ${USERNAME}/captcha-ocr-ultra:${TARGET_VERSION}