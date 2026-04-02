pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "pranavverma007"
        IMAGE_NAME     = "${DOCKERHUB_USER}/greetapi"
        IMAGE_TAG      = "${GIT_COMMIT[0..6]}"
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pip install flask pytest --quiet
                    pytest test_app.py -v
                '''
            }
        }

        stage('Build image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push image') {
            steps {
                sh '''
                    echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker logout
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    sed -i "s|IMAGE_PLACEHOLDER|${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml
                    kubectl apply -f k8s/
                    kubectl rollout status deployment/greetapi --timeout=60s
                '''
            }
        }

    }

    post {
        success {
            echo "Pipeline succeeded. App is running as ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed. Check the logs above."
        }
    }
}
