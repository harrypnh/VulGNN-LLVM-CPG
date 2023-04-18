import subprocess
import shutil
import json

def parse_repo_link(code_link):
    if code_link.split("//")[1].split("/")[0] == "git.altlinux.org":
        return f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('?p='))}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.ghostscript.com":
        return f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('?p='))}.git"

    elif code_link.split("//")[1].split("/")[0] == "git.hylafax.org":
        return f"git://{code_link.split('//')[1].split('?a=commit')[0]}"
    
    elif code_link.split("//")[1].split("/")[0] == "git.infradead.org":
        if len(code_link.split("//")[1].split(".git")[0].split("?p=")) >= 2:
            code_link = f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('?p='))}.git"
        else:
            code_link = f"git://{code_link.split('//')[1].split('.git')[0]}.git"
        
        repo = code_link.split('//')[1].split('.git')[0].split("/")[-1]
        if repo == "mtd-2.6":
            return "https://github.com/torvalds/linux.git"
        elif repo == "libtirpc":
            return "git://git.linux-nfs.org/projects/steved/libtirpc.git"
        elif repo == "openconnect":
            return "https://gitlab.com/openconnect/openconnect.git"
        elif repo == "libnl":
            return "https://github.com/thom311/libnl.git"
        else:
            return code_link
    
    elif code_link.split("//")[1].split("/")[0] == "git.linux-nfs.org":
        return f"git://{'projects/'.join(code_link.split('//')[1].split('.git')[0].split('?p='))}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.openafs.org":
        return f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('?p='))}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.savannah.nongnu.org":
        return f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('cgit/'))}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.wpitchoune.net":
        return f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('gitweb/?p='))}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "android.googlesource.com":
        if len(code_link.split("//")[1].split("/+/")[0].split("%2F")) >= 2:
            return f"https://{'/'.join(code_link.split('//')[1].split('/+/')[0].split('%2F'))}.git"
        else:
            return f"https://{code_link.split('//')[1].split('/+/')[0]}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "anongit.mindrot.org":
        return f"git://{code_link.split('//')[1].split('.git')[0]}.git"

    elif code_link.split("//")[1].split("/")[0] == "cgit.freedesktop.org":
        alternative_repo_srcs = {
            "accountsservice": "https://gitlab.freedesktop.org/accountsservice/accountsservice.git",
            "drm-misc": "git://anongit.freedesktop.org/drm/drm-misc",
            "exempi": "https://gitlab.freedesktop.org/libopenraw/exempi.git",
            "fontconfig": "https://gitlab.freedesktop.org/fontconfig/fontconfig.git",
            "harfbuzz": "git://anongit.freedesktop.org/harfbuzz",
            "harfbuzz.old": "git://anongit.freedesktop.org/harfbuzz.old",
            "libbsd": "https://gitlab.freedesktop.org/libbsd/libbsd.git",
            "pixman": "https://gitlab.freedesktop.org/pixman/pixman.git",
            "polkit": "https://gitlab.freedesktop.org/polkit/polkit.git",
            "systemd": "https://github.com/systemd/systemd.git",
            "udisks": "git://anongit.freedesktop.org/udisks",
            "virglrenderer": "https://gitlab.freedesktop.org/virgl/virglrenderer.git",
        }
        if len(code_link.split("//")[1].split("/commit")) == 2:
            code_link = f"https://{code_link.split('//')[1].split('/commit')[0].replace('cgit', 'gitlab')}.git"
        elif len(code_link.split("//")[1].split("/diff")) == 2:
            code_link = f"https://{code_link.split('//')[1].split('/diff')[0].replace('cgit', 'gitlab')}.git"
        repo = code_link.split('//')[1].split('.git')[0].split("/")[-1]
        
        if repo in alternative_repo_srcs:
            return alternative_repo_srcs[repo]
        else:
            return code_link
    
    elif code_link.split("//")[1].split("/")[0] == "cgit.kde.org":
        return f"https://{code_link.split('//')[1].split('.git')[0].replace('cgit.kde.org', 'github.com/KDE')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.busybox.net":
        return f"git://{code_link.split('//')[1].split('/commit/')[0]}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.enlightenment.org":
        return f"https://{code_link.split('//')[1].split('.git')[0].replace('apps/terminology', 'enlightenment/terminology').replace('core/enlightenment', 'enlightenment/enlightenment').replace('legacy/imlib2', 'old/legacy-imlib2')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.exim.org":
        return f"git://{code_link.split('//')[1].split('.git')[0]}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.gnupg.org":
        return f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('cgi-bin/gitweb.cgi?p='))}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.haproxy.org":
        return f"http://{code_link.split('//')[1].split('.git')[0].replace('?p=', 'git/')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.launchpad.net":
        return f"git://{code_link.split('//')[1].split('/commit/')[0]}"
    
    elif code_link.split("//")[1].split("/")[0] == "git.libav.org":
        alternative_repo_srcs = {
            "libav": "https://github.com/libav/libav.git",
        }
        code_link = f"git://{''.join(code_link.split('//')[1].split('.git')[0].split('?p='))}.git"
        repo = code_link.split('//')[1].split('.git')[0].split("/")[-1]
        if repo in alternative_repo_srcs:
            return alternative_repo_srcs[repo]
        else:
            return code_link
    
    elif code_link.split("//")[1].split("/")[0] == "git.libssh.org":
        return f"https://{code_link.split('//')[1].split('.git')[0]}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.lxde.org":
        return f"https://{''.join(code_link.split('//')[1].split('.git')[0].split('gitweb/?p=')).replace('git.lxde.org', 'github.com')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.lysator.liu.se":
        return f"https://{code_link.split('//')[1].split('/commit/')[0]}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.musl-libc.org":
        return f"https://{code_link.split('//')[1].split('/commit/')[0].replace('cgit/', 'git/')}"
    
    elif code_link.split("//")[1].split("/")[0] == "git.netfilter.org":
        return f"git://{code_link.split('//')[1].split('/commit/')[0]}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.openssl.org":
        return f"git://{code_link.split('//')[1].split('.git')[0].replace('gitweb/?p=', '').replace('?p=', '')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.pengutronix.de":
        return f"git://{code_link.split('//')[1].split('/commit/')[0].replace('cgit/', '')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.php.net":
        return f"https://{code_link.split('//')[1].split('.git')[0].replace('?p=', '').replace('git.php.net', 'github.com/php')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.postgresql.org":
        return f"git://{code_link.split('//')[1].split('.git')[0].replace('gitweb/?p=', 'git/')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.qemu.org":
        return f"git://{code_link.split('//')[1].split('.git')[0].replace('gitweb.cgi?p=', '').replace('?p=', '')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.quassel-irc.org":
        return f"git://{code_link.split('//')[1].split('.git')[0].replace('?p=', '')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.samba.org":
        return f"git://{code_link.split('//')[1].split('.git')[0].replace('?p=', '')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.savannah.gnu.org":
        alternative_repo_srcs = {
            "quagga": "https://github.com/Quagga/quagga.git",
            "weechat": "https://github.com/weechat/weechat.git"
        }
        code_link = f"git://{code_link.split('//')[1].split('.git')[0].replace('cgit/', '').replace('gitweb/?p=', '')}.git"
        repo = code_link.split('//')[1].split('.git')[0].split("/")[-1]
        if repo in alternative_repo_srcs:
            return alternative_repo_srcs[repo]
        else:
            return code_link
    
    elif code_link.split("//")[1].split("/")[0] == "git.shibboleth.net":
        return f"https://{code_link.split('//')[1].split('.git')[0].replace('view/?p=', 'git/')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.strongswan.org":
        return f"https://{code_link.split('//')[1].split('.git')[0].replace('git.strongswan.org/?p=', 'github.com/strongswan/')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "git.tartarus.org":
        return f"git://{code_link.split('//')[1].split('.git')[0].replace('?p=', '')}.git"
    
    elif code_link.split("//")[1].split("/")[0] == "github.com":
        alternative_repo_srcs = {
            "tomhughes_libdwarf": "https://github.com/davea42/libdwarf-code"
        }
        code_link = f"https://{'/'.join(code_link.split('//')[1].split('/')[0:3])}.git"
        repo = '_'.join(code_link.split('//')[1].split('.git')[0].split("/")[-2:])
        if repo in alternative_repo_srcs:
            return alternative_repo_srcs[repo]
        else:
            return code_link
    
    elif code_link.split("//")[1].split("/")[0] == "htcondor-git.cs.wisc.edu":
        return f"https://{code_link.split('//')[1].split('.git')[0].replace('htcondor-git.cs.wisc.edu/?p=condor', 'github.com/htcondor/htcondor')}.git"

def is_hex_str(str):
    try:
        int(str, 16)
        return True
    except ValueError:
        return False

def is_commit_id(str):
    return (is_hex_str(str) and len(str) <= 40) or (is_hex_str(str[:-1]) and len(str[:-1]) <= 40 and str[-1] == "^")

def parse_commit_hash(commit_str):
    if is_commit_id(commit_str):
        return commit_str
    elif len(commit_str.split("//")) > 1:
        if commit_str.split("//")[1].split("/")[0] == "android.googlesource.com":
            return commit_str.split("/+/")[1].split("/")[0].replace("%5E", "^")
        elif commit_str.split("//")[1].split("/")[0] == "cgit.freedesktop.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.savannah.gnu.org":
            if len(commit_str.split("id=")) == 2:
                return commit_str.split("id=")[1]
            else:
                return commit_str
        elif commit_str.split("//")[1].split("/")[0] == "git.launchpad.net":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "anongit.mindrot.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "cgit.kde.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.busybox.net":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.pengutronix.de":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.enlightenment.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.netfilter.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.savannah.nongnu.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.musl-libc.org":
            return commit_str.split("id=")[1]
        elif commit_str.split("//")[1].split("/")[0] == "git.libssh.org":
            return commit_str.split("id=")[1]
    elif len(commit_str.split("?w=")) > 1:
        return commit_str.split("?w=")[0]
    elif len(commit_str.split("#diff-")) > 1:
        return commit_str.split("#diff-")[0]
    else:
        return commit_str

def find_function_name(function_code):
    function_name = [token for token in function_code.split("(")[0].split(" ") if token != ""][-1]
    if function_name.find("*") != -1:
        function_name = function_name.split("*")[-1]
    function_name = function_name.replace("\n", "")
    function_name = function_name.replace("\t", "")
    return function_name

def generate_ir_and_cpg(args):
    def clean():
        try:
            shutil.rmtree(f"./repo_clone/{repo_dir_name}")
        except:
            return

    code_link, repo_dir_name, result_dir_name, version_pair_functions = args
    for version in version_pair_functions.keys():
        build_process = subprocess.run(
            args=["./ir_cpg_gen.sh", code_link, version, repo_dir_name, result_dir_name] + version_pair_functions[version],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if build_process.returncode != 0:
            with open(f"error_dump/{repo_dir_name}_{version}", "w") as error_dump:
                error_dump.write(build_process.stdout.decode(encoding="utf-8", errors="ignore"))
            last_error = build_process.stdout.decode(encoding="utf-8", errors="ignore").split("\n")[-2]
            if last_error not in ["Error: NO IR Found", "ERROR: llvm2cpg FAILED", "ERROR: joern FAILED"]:
                clean()
                return
        clean()

def cpg_dot2json(cpg_dot, json_format=False):
    cpg_json = {}
    cpg = cpg_dot.split('\n')
    function_name = cpg[0].split(' ')[1][1:-1]
    cpg_json['function'] = function_name
    cpg_json['nodes'] = []
    cpg_json['edges'] = []
    for cpg_line in cpg[1:]:
        if cpg_line == '}' or cpg_line == '':
            continue
        if '\" -> \"' in cpg_line:
            node_from = cpg_line.split('\" -> \"')[0].split('\"')[-1]
            node_to = cpg_line.split('\" -> \"')[-1].split('\"  [ label = \"')[0]
            edge_feature = cpg_line.split('[ label = \"')[-1].split('\"]')[0]
            if edge_feature.find(':') == -1:
                cpg_json['edges'].append({'from_id': node_from, 'to_id': node_to, 'feature': edge_feature})
            elif edge_feature[edge_feature.find(':') + 1:] == ' ':
                edge_type = edge_feature[:edge_feature.find(':')]
                cpg_json['edges'].append({'from_id': node_from, 'to_id': node_to, 'type': edge_type})
            else:
                edge_type = edge_feature[:edge_feature.find(':')]
                edge_feature = edge_feature[edge_feature.find(':') + 2:]
                edge_feature = edge_feature.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '\"').replace('&amp;', '&')
                cpg_json['edges'].append({'from_id': node_from, 'to_id': node_to, 'type': edge_type, 'feature': edge_feature})
        else:
            node_id = cpg_line.split(' ')[0][1:-1]
            node_feature = cpg_line.split('[label = <(')[-1]
            node_feature = node_feature[:len(node_feature) - node_feature[::-1].find(')') - 1]
            node_feature = node_feature.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '\"').replace('&amp;', '&')
            cpg_json['nodes'].append({'id': node_id, 'feature': node_feature})
    if json_format:
        return json.dumps(cpg_json)
    return cpg_json