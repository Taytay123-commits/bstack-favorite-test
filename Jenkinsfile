pipeline {
    agent any

    environment {
        BROWSERSTACK_USERNAME = credentials('bstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('bstack-access-key')
    }



        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                withEnv([
                    "BROWSERSTACK_USERNAME=${env.BROWSERSTACK_USERNAME}",
                    "BROWSERSTACK_ACCESS_KEY=${env.BROWSERSTACK_ACCESS_KEY}"
                ]) {
                    sh 'pytest'
                }
            }
        }
    }
}
