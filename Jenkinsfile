pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        CODECOV_TOKEN = credentials('codecov-token')
    }

    stages {
        stage('Verificar dependencias') {
            steps {
                sh '''
                    docker version
                    docker-compose version
                '''
            }
        }

        stage('Construir contenedores') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                sh '''
                    docker-compose run --rm backend \
                    bash -c "cd /app && pytest -v --cov=. --cov-branch \
                    --cov-report=xml:/app/coverage.xml --cov-report=term-missing"
                '''
                // Copiar el coverage.xml del contenedor al workspace
                sh '''
                    docker cp $(docker-compose ps -q backend):/app/coverage.xml ./coverage.xml || \
                    docker run --rm -v $(pwd):/workspace office-access-setup-backend \
                    cp /app/coverage.xml /workspace/coverage.xml
                '''
            }
        }

        stage('Subir Coverage a Codecov') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "=== Verificando coverage.xml ==="
                    ls -la coverage.xml
                    cat coverage.xml | head -n 20
                    
                    # Descargar Codecov CLI
                    curl -Os https://cli.codecov.io/latest/linux/codecov
                    chmod +x codecov
                    
                    # Subir con información adicional
                    ./codecov upload-process \
                        -f coverage.xml \
                        -t "$CODECOV_TOKEN" \
                        --plugin pycoverage \
                        --dir backend
                '''
            }
        }

        stage('Desplegar') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            sh 'docker-compose down --volumes --remove-orphans || true'
            echo 'Pipeline terminado'
        }
    }
}
