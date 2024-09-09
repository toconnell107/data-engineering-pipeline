pipeline {
    agent any // This specifies the Jenkins agent or node where the pipeline will run. 'any' means any available agent.

    stages {
        stage('Checkout') {
            steps {
                // Check out code from version control
                git branch: "main", credentialsId: "github-credentials", url: "https://github.com/toconnell107/data-engineering-pipeline.git"
            }
        }

        stage('Install Dependencies') {
            steps {
                // Execute build commands
                script {
                    docker.image('python3.8').inside {
                        sh 'pip install -r scripts/requirements.txt'
                    }
                } 
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image('python3.8').inside {
                        sh 'python -m unittest discover -s scripts'
                    }
                } 
            }
        }

        stage('Run ETL') {
            steps {
                script {
                    docker.image('python3.8').inside {
                        sh 'python scripts/etl.py'
                    }
                } 
            }
        }

    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.csv', allowEmptyArchive: true
        }
    }
}

