docker_pull() {
    docker pull $1
    docker tag $1 $HARBOR_URL/$HARBOR_PROJECT/$2:latest
    docker push $HARBOR_URL/$HARBOR_PROJECT/$2:latest
}

docker_build() {
    docker build -t $2 $1
    docker tag $2:latest $HARBOR_URL/$HARBOR_PROJECT/$2:latest
    docker push $HARBOR_URL/$HARBOR_PROJECT/$2:latest
}


ku() {
    kubectl --kubeconfig ${HOME}/${CLUSTER_NAME}-kubeconfig -n ${NAMESPACE} $@
}
    
ko() {
    kubectl --kubeconfig ${HOME}/org-1-admin-kubeconfig -n ${NAMESPACE} $@
}

kp() {
    kubectl --kubeconfig ${HOME}/org-1-admin-kubeconfig -n platform $@
}

kustomize() {
    if [ "$2" = "kustomize/projects" ]; then
        kp apply -k $@
    else
        ku apply -k $@
    fi
}

apply() {
    if [ "$2" = "platform" ]; then
        for f in $1/*.yaml; do envsubst < $f | ko -n "platform" apply -f -; done
    else
        for f in $1/*.yaml; do envsubst < $f | ku apply -f -; done
    fi
}

delete() {
    if [ "$2" = "platform" ]; then
        for f in $1/*.yaml; do envsubst < $f | ko -n "platform" delete -f -; done
    else
        for f in $1/*.yaml; do envsubst < $f | ku delete -f -; done
    fi    
}

restart() {
    if [ "$2" = "platform" ]; then
        for f in $1/*.yaml; do envsubst < $f | ko -n "platform" rollout restart -f -; done
    else
        for f in $1/*.yaml; do envsubst < $f | ku rollout restart -f -; done
    fi
}

