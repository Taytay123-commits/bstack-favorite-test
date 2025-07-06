pipeline {
    agent any

    environment {
        BROWSERSTACK_USERNAME = credentials('bstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('bstack-access-key')
        DEMO_USERNAME = credentials('bstack-demo-username')
        DEMO_PASSWORD = credentials('bstack-demo-password')
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
                    "BROWSERSTACK_ACCESS_KEY=${env.BROWSERSTACK_ACCESS_KEY}",
                    "DEMO_USERNAME=${env.DEMO_USERNAME}",
                    "DEMO_PASSWORD=${env.DEMO_PASSWORD}"
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
