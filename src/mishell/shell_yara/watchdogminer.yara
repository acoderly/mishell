rule watchdogminer
{
meta:
    author="vxpeek@gmail.com"
    data = "2021/3/18"
//https://unit42.paloaltonetworks.com/watchdog-cryptojacking/

strings:
	$shbang_1 = {23 21 [-] 2F 62 69 6E 2F 62 61 73 68} //"#!/bin/bash"
	$shbang_2 = {23 21 [-] 2F 62 69 6E 2F 73 68} //"#!/bin/sh"
	$shbang_3 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 73 68} //"#!/usr/bin/sh"
	$shbang_4 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 62 61 73 68} //"#!/usr/bin/bash"
	$anchor_watchdogminer_dl = "miner_url"
	$anchor_config = "config_url"
	$anchor_watchdogminer_sh = "sh_url"
	$anchor_rsa = "echo \"ssh-rsa"
	$anchor_wallet = "./zzh "
condition:
	for any of ($shbang_*):($ at 0) and
	(1 of ($anchor_*))
}
