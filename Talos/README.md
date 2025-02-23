# Talos

## Apply a config with tailscale

```
$ cat patch.yaml
apiVersion: v1alpha1
kind: ExtensionServiceConfig
name: tailscale
environment:
  - TS_AUTHKEY=xxxx

$ talosctl apply-config -f controlplane.yaml -p @patch.yaml                                                                      
Applied configuration without a reboot
```

Always apply with the patch file, otherwise, tailscale config will be deleted.

## Install ad-ons

Go to [Talos factory](https://factory.talos.dev/) and select the extension you want

Go to the `Upgrading Talos Linux` section and copy the image name :

Execute 

```
$ talosctl upgrade --image <image-name:tag> -m powercycle -f
◱ watching nodes: [100.101.249.122]
    * 100.101.249.122: waiting for actor ID
```

It should stop, just wait a bit and the cluster should be up with the new config

## Upgrade 

Select the new image you want 

Delete all pods using nfs mount point

Execute `talosctl upgrade --nodes 100.101.249.122 --image factory.talos.dev/installer/4a0d65c669d46663f377e7161e50cfd570c401f26fd9e7bda34a0216b6f1922b:v1.9.4`
