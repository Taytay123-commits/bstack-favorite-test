pipeline {
    agent any

    environment {
        BROWSERSTACK_USERNAME = credentials('bstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('bstack-access-key')
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                withEnv([
                    "BROWSERSTACK_USERNAME=${env.BROWSERSTACK_USERNAME}",
                    "BROWSERSTACK_ACCESS_KEY=${env.BROWSERSTACK_ACCESS_KEY}"
                ]) {
                    sh '''
                        . venv/bin/activate
                        pytest tests/
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            echo 'Build failed — check console output for details.'
        }
    }
}
