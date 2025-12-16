pipeline {
    agent any

    stages {
        stage('Clean Workspace') {
            steps {
                script {
                    cleanWs()  // Cleans the workspace before anything else
                }
            }
        }

        stage('Cloning the Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Tulajaram12/code_repo.git'
            }
        }

        stage('Build the Code') {
            steps {
                script {
                    // Login to AWS ECR
                    sh '''
                        aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 484468819850.dkr.ecr.ap-south-1.amazonaws.com
                    '''

                    // Build the Docker image
                    sh '''
                        docker build -t new_namespace/repo22 .
                    '''

                    // Tag the Docker image correctly
                    sh '''
                        docker tag new_namespace/repo22:latest 484468819850.dkr.ecr.ap-south-1.amazonaws.com/namespace/repo22:v$BUILD_NUMBER
                    '''

                    // Push the Docker image to AWS ECR
                    sh '''
                        docker push 484468819850.dkr.ecr.ap-south-1.amazonaws.com/namespace/repo22:v$BUILD_NUMBER
                    '''
                }
            }
        }

        stage('Setting the Image Version') {
            steps {
                script {
                    // Clone the Helm repository
                    sh 'git clone https://github.com/Tulajaram12/helm.git'
                    sh 'ls -l'  // List files to verify it's cloned

                    // Update values.yaml with the new image version (using double quotes for Groovy interpolation)
                    sh """
                        cd helm && sudo sed -i 's|tag: \".*\"|tag: \"v$BUILD_NUMBER\"|' webapp/values.yaml
                        ls -al  # List files to verify the update
                        cat webapp/values.yaml
                    """
                    
                    // Commit the changes and push them back to GitHub
                    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                        sh """
                            cd helm
                            git config --global user.name "Tulajaram12"
                            git config --global user.email "tulajaramkamble@gmail.com"
                            git remote set-url origin https://$GITHUB_TOKEN@github.com/Tulajaram12/helm.git
                            git add .
                            git commit -m "updating image version v$BUILD_NUMBER"
                            git push origin main
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Clean the workspace after the pipeline completes, if needed
        }
    }
}

