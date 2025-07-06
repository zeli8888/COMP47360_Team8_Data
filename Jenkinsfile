pipeline{

  agent any
  environment {
    version = '1.0'
  }

  stages{

    stage('Test'){
      steps{
        script {
            sh 'docker build -t planhattan-ml-test -f TestDockerfile .'
            def testExitCode = sh(
                script: 'docker run --rm planhattan-ml-test',
                returnStatus: true
            )
            
            if (testExitCode != 0) {
                error "测试失败，退出码: ${testExitCode}"
            }

            sh 'docker rmi planhattan-ml-test'
        }
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
