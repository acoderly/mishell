rule sysrv_sh
{
/**
MD5:
    479bd3aa6c1d5fddfa9d4b3c4c2065ae
*/
meta:
    author = "vxpeek@gmail.com"
    refer = "https://mp.weixin.qq.com/s/95XHvKCEWLu7V8owkDwSUw, https://mp.weixin.qq.com/s/iNqBcLKwhVUSz5ltLN_ubw"

strings:
    $anchor_cc = "cc="
    $anchor_config = "{\"url\": "
    $anchor_persistent = "echo \"*/"
    $anchor_get = "get $cc/"
    $anchor_get_1 = "get \"$cc/"
condition:
    1 of them
}