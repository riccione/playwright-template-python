pipeline {
    agent {
        docker {
            image 'python:3.13-slim'
            args '-v /var/tmp/uv-cache:/custom-cache-dir -v /var/tmp/playwright-cache:/custom-playwright-dir'
        }
    }

    environment {
        UV_CACHE_DIR             = '/custom-cache-dir'
        PLAYWRIGHT_BROWSERS_PATH = '/custom-playwright-dir'
        PATH                     = "/root/.local/bin:${env.PATH}"
        BASE_URL                 = 'https://playwright.dev/'
        ADMIN_USER               = credentials('JENKINS_ADMIN_USER')
        ADMIN_PASSWORD           = credentials('JENKINS_ADMIN_PASSWORD')
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        ansiColor('xterm')
    }

    stages {
        stage('Initialize & Install') {
            steps {
                script {
                    sh 'apt-get update && apt-get install -y curl git'
                    sh 'curl -LsSf https://astral.sh/uv/install.sh | sh'
                    sh 'uv sync --frozen'
                    sh 'uv run playwright install --with-deps'
                }
            }
        }

        stage('Lint') {
            steps {
                sh 'uv run ruff check .'
            }
        }

        stage('Format Check') {
            steps {
                sh 'uv run ruff format --check .'
            }
        }

        stage('Execute Regression Suite') {
            steps {
                sh 'uv run pytest --alluredir=allure-results'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test-results/**, reports/**', allowEmptyArchive: true, fingerprint: true
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
