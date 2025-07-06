pipeline{

  agent any
  environment {
    version = '1.0'
  }

  stages{

    stage('Test'){
      steps{
        sh '/usr/bin/python3.12 -m pip install -r requirements.txt'
        sh 'pytest prediction_controller_test.py -v'
      }
    }

    stage('Build Docker Image'){
      steps{
        sh "docker build -t planhattan-ml:${version} ."
        sh "docker tag planhattan-ml:${version} zeli8888/planhattan-ml:${version}"
        sh "docker push zeli8888/planhattan-ml:${version}"
        sh "docker image prune -f"
      }
    }

    stage('Run Docker Container'){
      steps{
        sh script: 'docker stop planhattan-ml', returnStatus: true
        sh script: 'docker rm planhattan-ml || true', returnStatus: true
        sh "export version=${version} && docker-compose -p planhattan -f planhattan-ml.yaml up -d --force-recreate"
      }
    }
  }
}
