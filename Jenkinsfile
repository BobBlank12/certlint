pipeline {
  agent any
  stages {
    stage("Read the properties file") {
      steps {
        script {
          def props = readProperties file: 'PROPERTIES'
          env.VERSION = props.VERSION
          env.PROJECT = props.PROJECT
          env.LOCATION = props.LOCATION
          env.REPOSITORY = props.REPOSITORY
          env.IMAGE = props.IMAGE
          env.CLUSTER = props.CLUSTER
        }
      }
    }
    stage("Build the Docker image") {
      steps {
        echo 'Building the application...'
        // I had a problem here if my cluster was not 1.26, the uploads folder under website was getting deleted.
        //sh 'pwd'
        //sh 'ls -la website'
        //sh 'ls -la website/uploads'
        sh 'docker stop ${IMAGE}:${VERSION} || exit 0'
        sh 'docker rm ${IMAGE}:${VERSION} || exit 0'
        sh 'docker build --tag ${IMAGE}:${VERSION} .'
      }
    }
    stage("test") {
      steps {
        echo 'testing the application...'
      }
    }
    stage("Tag and Push the image to GCP Artifact registry") {
      // I got the idea to use a SECRET FILE from here:
      //    https://stackoverflow.com/questions/45355007/how-to-authenticate-with-a-google-service-account-in-jenkins-pipeline
      // The official Google method using all of their plugins is here:
      //    https://cloud.google.com/kubernetes-engine/docs/archive/continuous-delivery-jenkins-kubernetes-engine
      steps {
        echo 'Pushing the application to GCP Artifact Registry'
        sh 'docker tag ${IMAGE}:${VERSION} ${LOCATION}-docker.pkg.dev/${PROJECT}/${REPOSITORY}/${IMAGE}:${VERSION}'
        script {
          withCredentials([file(credentialsId: "${PROJECT}", variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud auth configure-docker ${LOCATION}-docker.pkg.dev')
            //sh('gcloud artifacts docker images delete --quiet ${LOCATION}-docker.pkg.dev/${PROJECT}/${REPOSITORY}/${IMAGE}:${VERSION} --delete-tags || exit 0')
            sh('docker push ${LOCATION}-docker.pkg.dev/${PROJECT}/${REPOSITORY}/${IMAGE}:${VERSION}')
          }
        }
      }
    }
    stage("DELETE and re-deploy to GKE"){
      steps {
        echo 'Deploying the container to GKE'
        script {
          withCredentials([file(credentialsId: "${PROJECT}", variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud container clusters get-credentials ${CLUSTER} --zone=${LOCATION}-c --project=${PROJECT}')
            sh('kubectl delete deployment ${IMAGE} || exit 0')
            // Use sed to replace the $VERSION placeholder in the K8S application manifest file...
            //sh('sed "s/\\$VERSION/${VERSION}/" ${IMAGE}-application.yml')
            sh('sed "s/\\$VERSION/${VERSION}/" ${IMAGE}-application.yml | kubectl apply -f -')
            sh('kubectl apply -f ${IMAGE}-service.yml')
          }
        }
      }
    }
  }
}