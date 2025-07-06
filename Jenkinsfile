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
                withCredentials([usernamePassword(credentialsId: 'bstack-demo-login', 
                                                  usernameVariable: 'DEMO_USER', 
                                                  passwordVariable: 'DEMO_PASS')]) {
                    withEnv([
                        "BROWSERSTACK_USERNAME=${env.BROWSERSTACK_USERNAME}",
                        "BROWSERSTACK_ACCESS_KEY=${env.BROWSERSTACK_ACCESS_KEY}",
                        "DEMO_USER=${env.DEMO_USER}",
                        "DEMO_PASS=${env.DEMO_PASS}"
                    ]) {
                        sh '''
                            . venv/bin/activate
                            PYTHONPATH=. pytest tests/
                        '''
                    }
                }
            }
        }
    }
}

