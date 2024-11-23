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
