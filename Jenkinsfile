pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('psvimal33329-dockerhub')
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t psvimal33329/fastapi:latest .'
      }
    }
    stage('Login') {
      steps {
        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
      }
    }
    stage('Push') {
      steps {
        sh 'docker push psvimal33329/fastapi:latest'
      }
    }
  }
  post {
    always {
      sh 'docker logout'
    }
  }
}