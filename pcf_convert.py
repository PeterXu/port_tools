#!/usr/bin/python
# uskee.org
#

import os
import sys
import ConfigParser
from xml.dom.minidom import Document

# To gen one xml element
def elem(doc, parent, tag):
	elem = doc.createElement(tag)
	parent.appendChild(elem) 
	return elem

# To gen one xml element with text
def elem_text(doc, parent, tag, text):
	elem = doc.createElement(tag)
	node = doc.createTextNode(text)
	elem.appendChild(node)
	parent.appendChild(elem) 
	return elem

# To format output xml lines
class Writer:
	def __init__(self, fname):
		self._f = file(fname, "w")
		self._start = 0
		self._lkeys = []
		self._rkeys = []

		keys = ["key", "string", "data"]
		for k in keys:
			self._lkeys.append("<%s" % k)
			self._rkeys.append("</%s>" % k)

	def write(self, str):
		tstr = str.strip()
		if tstr in self._lkeys:
			self._start = 1
			str = str.rstrip()
		elif tstr in self._rkeys:
			self._start = 0
			str = str.lstrip()
		elif self._start == 1:
			str = tstr
		if self._f:
			self._f.write(str)
			
	def close(self):
		if self._f:
			self._f.close()

def xml(fname, keys):
	doc = Document()
	wtr = Writer(fname)

	# fill base
	plist = elem(doc, doc, "plist")
	plist.setAttribute("version", "1.0")

	dict = elem(doc, plist, "dict")
	key = elem_text(doc, dict, "key", "IPSec")
	dict = elem(doc, dict, "dict")
	key = elem_text(doc, dict, "key", "SystemConfig")
	dict = elem(doc, dict, "dict")
	key = elem_text(doc, dict, "key", "IPSec")
	dict = elem(doc, dict, "dict")

	# fill vpn setting
	key = elem_text(doc, dict, "key", "AuthenticationMethod")
	string = elem_text(doc, dict, "string", "SharedSecret")
	key = elem_text(doc, dict, "key", "ExportedSharedSecret")
	data = elem_text(doc, dict, "data", keys["data"])

	key = elem_text(doc, dict, "key", "LocalIdentifier")
	string = elem_text(doc, dict, "string", keys["LocalIdentifier"])
	key = elem_text(doc, dict, "key", "LocalIdentifierType")
	string = elem_text(doc, dict, "string", "KeyID")
	key = elem_text(doc, dict, "key", "RemoteAddress")
	string = elem_text(doc, dict, "string", keys["RemoteAddress"])
	key = elem_text(doc, dict, "key", "SharedSecret")
	string = elem_text(doc, dict, "string", keys["SharedSecret"])
	key = elem_text(doc, dict, "key", "SharedSecretEncryption")
	string = elem_text(doc, dict, "string", "Keychain")
	key = elem_text(doc, dict, "key", "XAuthName")
	string = elem_text(doc, dict, "string", "Prompt")
	key = elem_text(doc, dict, "key", "XAuthPasswordEncryption")
	string = elem_text(doc, dict, "string", "Prompt")
	
	doc.writexml(wtr, indent="", addindent="\t", newl="\n")
	wtr.close()


def proc_pcf(fname):
	cfg = ConfigParser.ConfigParser()
	cfg.read(fname)

	keys = {}
	keys["name"] = cfg.get("main", "Description")
	enc = cfg.get("main", "enc_GroupPwd")
	err = os.system("./cisco-decrypt %s > /tmp/vpn.txt" % enc)
	if err != 0:
		return False
	fdec = file("/tmp/vpn.txt")
	keys["data"] = fdec.read().strip()
	keys["LocalIdentifier"] = cfg.get("main", "GroupName")
	keys["RemoteAddress"] = cfg.get("main", "Host")
	keys["SharedSecret"] = "88B4384D-4CCC-4F1A-85C5-5F54724D3952.SS"
	
	basename = os.path.splitext(os.path.basename(fname))
	xml("%s.networkConnect" % basename[0], keys);
	return True


if __name__ == '__main__':
	if not os.path.exists("./cisco-decrypt"):
		print "cisco-decrypt is not exist, pls check current path or build it referred in cisco_decrypt.c"
		sys.exit(1)
	if len(sys.argv) != 2:
		print "usage: %s file|dir" % sys.argv[0]
		sys.exit(1)

	fdir = sys.argv[1]
	if not os.path.isdir(fdir) and os.path.exists(fdir):
		proc_pcf(fdir)
	else:
		print "currently not support dir"
	sys.exit(0)
