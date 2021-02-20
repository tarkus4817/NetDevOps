from nornir_scrapli.tasks import netconf_get
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.tasks.files import write_file
import xmltodict
import pprint
import simplejson as json
import yaml
from collections import OrderedDict



nr = InitNornir(config_file="nornir_data/config.yaml")



def yang_sucks(task):

   pp= pprint.PrettyPrinter(indent=4)
   result = task.run(task=netconf_get, filter_= "/native/ntp", filter_type="xpath")
   task.run(task=write_file, content=result.result, filename=f"host_vars/{task.host}.xml")
   #yaml = YAML(typ="safe")

   with open(f"host_vars/{task.host}.xml") as fd:     
     doc=xmltodict.parse(fd.read())
   correct_link = "_xmlns"
   doc2 = doc["rpc-reply"]["data"]
   for i in doc2["native"]:
     if i != "@xmlns":
       feature = i
       doc2["native"][i].update({"_operation":"replace"})
       doc2["native"][i].move_to_end("_operation", last=False)
   doc_copy= {}
   doc_copy["native"]=doc2["native"].copy()
  # pp.pprint(json.dumps(doc_copy))
   for first_layer in doc_copy["native"]:
     
     if first_layer == "@xmlns":
       doc2["native"]["_xmlns"] = doc2["native"]["@xmlns"]
       del doc2["native"]["@xmlns"]
       for second_layer in  doc_copy["native"][feature]:
         print(second_layer)
         
         for third_layer in doc_copy["native"][feature][second_layer]:
           print(third_layer)
           if third_layer == "@xmlns":
             doc2["native"][i][second_layer]["_xmlns"] = doc2["native"][i][second_layer]["@xmlns"]
             pp.pprint(json.dumps(doc2))
             #del doc2["native"][i][second_layer]["@xmlns"]
         
         


       
             print("poop")
       








   #for i in doc2["native"]:
   #  if i != "@xmlns":
   #    print(i)
   #    new_dict["native"][i] = {}
   #    new_dict["native"][i]["_operation"] = "replace"
   #    for j in doc2["native"][i]:
   #      for k in doc2["native"][i][j]:
   #        new_dict["native"][i][j] = k
   #doc3 = {}
   #doc3["native"] = {}
  
   #doc3["native"]["router"]["_operation"] = "replace"
   with open(f"host_vars/router/{task.host}.xml", "w") as f:
     f.write(json.dumps(doc2, indent=4, sort_keys=False))

  #pp.pprint(json.dumps(doc2))
   #pp.pprint(json.dumps(new_dict))








   #with open(f"host_vars/router/{task.host}.yaml", "w") as y:
   #  yaml.dump(doc2, json_data)



   #path = (f"host_vars/router/{task.host}.xml")
   #yaml.dump(doc2, path)
   #with open(f"host_vars/router/{task.host}.xml", "w") as f:
   #  file = yaml.dump(doc2)
   #  f.write(file)
   
   #with open(f"host_vars/router/{task.host}.xml", "w") as f:
   #  f.write(simplejson.dumps(doc2, indent=4, sort_keys=True))
   #pp= pprint.PrettyPrinter(indent=4)
   #pp.pprint(json.dumps(doc2))
   #with open(f"host_vars/router/{task.host}.xml") as f:
   #   f.write(fin)

   #tree=ET.parse(f"host_vars/{task.host}.xml")
   #root=tree.getroot()
   #print(root)
   #print(root.tag)
   #for elem in root:
     #print(elem.tag, elem.attrib)
     #print(ET.tostring(elem, encoding="utf8").decode("utf8"))
     #test = ET.tostring(elem, encoding="utf8").decode("utf8")
     #for subelem in elem:
       #test = ET.tostring(subelem, encoding="utf8").decode("utf8")
       #print(test)
       #print(subelem.tag, subelem.attrib)
       #for subsub in subelem:
         #print(subsub.tag, subsub.attrib)
         #for s in subsub:
           #print(s.tag, s.attrib)
   #task.run(task=write_file, content=test, filename=f"host_vars/router/{task.host}.xml")
  # print(ET.tostring(root, encoding="utf8").decode("utf8"))
   #task.run(task=write_file, content=doc, filename=f"host_vars/router/{task.host}.xml")





   return result

spine = nr.filter (F(groups__contains="spine"))
result = spine.run(task=yang_sucks)

print_result(result)


