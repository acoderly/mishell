private rule shell_scanner_aa
{
meta:
    author="vxpeek@gmail.com"
    data = "2021/4/23"
//md5:4d9a348877a07c2052639dc7eb6fbd03

strings:
	$shbang_1 = {23 21 [-] 2F 62 69 6E 2F 62 61 73 68} //"#!/bin/bash"
	$shbang_2 = {23 21 [-] 2F 62 69 6E 2F 73 68} //"#!/bin/sh"
	$shbang_3 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 73 68} //"#!/usr/bin/sh"
	$shbang_4 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 62 61 73 68} //"#!/usr/bin/bash"
	$scanner_1 = "masscan --max-rate 10000 -p6379"
	$cmd_1 = "cat .dat | redis-cli -h"

condition:
	for any of ($shbang_*):($ at 0) and
	(#scanner_1 > 2) and
	(#cmd_1 > 3) and
	filesize < 10KB
}

private rule watchdogminer_scanner_a
{
meta:
    author="vxpeek@gmail.com"
    data = "2021/4/23"
//md5:2572763dfb83e387723f8eeb7ec758c9

strings:
	$shbang_1 = {23 21 [-] 2F 62 69 6E 2F 62 61 73 68} //"#!/bin/bash"
	$shbang_2 = {23 21 [-] 2F 62 69 6E 2F 73 68} //"#!/bin/sh"
	$shbang_3 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 73 68} //"#!/usr/bin/sh"
	$shbang_4 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 62 61 73 68} //"#!/usr/bin/bash"
	$chattr_1 = "chattr -i /usr/bin/ip6network"
	$chattr_2 = "chattr -i /usr/bin/kswaped"
	$chattr_3 = "chattr -i /usr/bin/irqbalanced"
	$chattr_4 = "chattr -i /usr/bin/rctlcli"
	$chattr_5 = "chattr -i /usr/bin/systemd-network"
	$chattr_6 = "chattr -i /usr/bin/pamdicks"
	$kill_1 = "echo 1 > /usr/bin/ip6network"
	$kill_2 = "echo 2 > /usr/bin/kswaped"
	$kill_3 = "echo 3 > /usr/bin/irqbalanced"
	$kill_4 = "echo 4 > /usr/bin/rctlcli"
	$kill_5 = "echo 5 > /usr/bin/systemd-network"
	$kill_6 = "echo 6 > /usr/bin/pamdicks"
	$scan_1 = "Masscan" nocase
	$scan_2 = "Pnscan" nocase

condition:
	for any of ($shbang_*):($ at 0) and
	(2 of ($chattr_*)) and
	(2 of ($kill_*)) and
	(all of ($scan_*)) and
	filesize < 10KB

}

rule watchdogminer_scanner
{
meta:
    author="vxpeek@gmail.com"
    data = "2021/4/23"
//md5:d48bd6eb5f17865a63839d126df6cf89

strings:
	$shbang_1 = {23 21 [-] 2F 62 69 6E 2F 62 61 73 68} //"#!/bin/bash"
	$shbang_2 = {23 21 [-] 2F 62 69 6E 2F 73 68} //"#!/bin/sh"
	$shbang_3 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 73 68} //"#!/usr/bin/sh"
	$shbang_4 = {23 21 [-] 2F 75 73 72 2F 62 69 6E 2F 62 61 73 68} //"#!/usr/bin/bash"
	$chattr_1 = "chattr -i /usr/bin/ip6network"
	$chattr_2 = "chattr -i /usr/bin/kswaped"
	$chattr_3 = "chattr -i /usr/bin/irqbalanced"
	$chattr_4 = "chattr -i /usr/bin/rctlcli"
	$chattr_5 = "chattr -i /usr/bin/systemd-network"
	$chattr_6 = "chattr -i /usr/bin/pamdicks"
	$kill_1 = "echo 1 > /usr/bin/ip6network"
	$kill_2 = "echo 2 > /usr/bin/kswaped"
	$kill_3 = "echo 3 > /usr/bin/irqbalanced"
	$kill_4 = "echo 4 > /usr/bin/rctlcli"
	$kill_5 = "echo 5 > /usr/bin/systemd-network"
	$kill_6 = "echo 6 > /usr/bin/pamdicks"
	$name = "ftp://ftp.lysator.liu.se/pub/unix/pnscan/pnscan"
    $anchor_backup = "echo 'set backup"
    $anchor_bbdir = "$bbdir -fsSL"
condition:
	shell_scanner_aa or
	watchdogminer_scanner_a or
	for any of ($shbang_*):($ at 0) and
	(2 of ($chattr_*)) and
	(2 of ($kill_*)) and
	$name and
	(1 of ($anchor_*)) and
	filesize < 10KB
}
