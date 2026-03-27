pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '362437996214'
        ECR_REPO = 'url-shortener'
        IMAGE_TAG = "${GIT_COMMIT[0..6]}"
        IMAGE_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
        EKS_CLUSTER_NAME = 'vdgM-eks-cluster'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_URI} .
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push ${IMAGE_URI}
                '''
            }
        }
    
        stage('Deploy to EKS') {
            steps {
                sh '''
                    aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}

                    sed "s|<IMAGE_URI>|${IMAGE_URI}|g" deployment.yaml | kubectl apply -f -
                    kubectl apply -f service.yaml
                '''
            }
        }
    }
    post {
        success {
            echo "Image pushed successfully: ${IMAGE_URI}"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}