from git import Repo
import ruamel.yaml
import os

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

def new_image_data(image_name, new_name, new_tag):
    return {
        'name': image_name,
        'newName': new_name,
        'newTag': new_tag
    }


def update_image(data, image_name, new_name, new_tag):
    if 'images' in data:
        updated = False
        for image in data['images']:
            if(image['name'] == image_name):
                image.update(new_image_data(image_name, new_name, new_tag))
                updated = True
        if(not updated):
            data['images'].append(new_image_data(image_name, new_name, new_tag))
    else:
        data.update({
            'images': [new_image_data(image_name, new_name, new_tag)]
        })

    return data

    
def get_manifest(data, file = None):
    return yaml.dump(data, file)

def update_manifest(data, path):
    with open(path, 'w') as file:
        yaml.dump(data, file)
    

def git_push(path_to_repo, commit_message):
    try:
        repo = Repo(path_to_repo)
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    


path_to_repo = 'manifests'
def clone_repo(path):
    cloned_repo = Repo.clone_from("git@github.com:MicroLauncher/kube-manifest.git",
                                  path)
    return cloned_repo

clone_repo(path_to_repo)

with open('manifests/devex/sample-app/overlays/staging/kustomization.yaml', 'r') as file:
    deployment_yaml = yaml.load(file)


update_manifest(update_image(deployment_yaml, "sample/sample_app", "rohitlavu/app", os.getenv("CIRCLE_SHA1")[0:7]), 'manifests/devex/sample-app/overlays/staging/kustomization.yaml')

git_push(path_to_repo, "update image")