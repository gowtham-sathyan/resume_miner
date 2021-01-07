from pdfminer.high_level import extract_text
import re
import stanza
def extract(filename):
	nlp = stanza.Pipeline('en')
	pdf_text=extract_text(filename)
	text_1=re.sub("\s\s\s+" , "\n", pdf_text)
	text_1=text_1.split("\n")
	text=[]
	i=0
	while i<len(text_1):
		status_flag=0
		j=text_1[i].strip()
		if j=="" or j==" ":
			text_1.remove(text_1[i])
		else:
			while status_flag==0:
				ind=len(j)-1
				while j[ind]==" ":
					ind=ind-1
				if j[ind]!="," or i==len(text_1)-1:
					text.append(j)
					i+=1
					status_flag=1
				else:
					j+=text_1[i+1].strip()
					i+=1
	t_list=["gpe", "org"]
	skipped=[]
	result=set()
	org_flag=0
	loc_flag=0
	for i in text:
		doc=nlp(i)
		doc_list=doc.to_dict()
		wanted_flag=0
		date_flag=0
		unwanted_counter=0
		dob_counter=0
		num_counter=0
		for j in range(len(doc_list)):
			for k in doc_list[j]:
				try:
					if k["upos"]!="PUNCT":
						if "gpe" not in k["ner"].lower():
							loc_flag=0
						if "date" in k["ner"].lower():
							if k["ner"]=="S-DATE":
								pass
							elif k["ner"]=="B-DATE":
								dob_counter+=1
								if k["upos"]=="NUM":
									num_counter+=1
								elif k["upos"]!="PUNCT":
									month_flag=k["upos"]
							elif k["ner"]=="I-DATE" and dob_counter==1:
								dob_counter+=1
								if k["upos"]=="NUM":
									num_counter+=1
								elif k["upos"]!="PUNCT":
									month_flag=k["upos"]
							elif k["ner"]=="E-DATE" and dob_counter==2:
								if k["upos"]=="NUM":
									num_counter+=1
								elif k["upos"]!="PUNCT":
									month_flag=k["upos"]
								if (num_counter==2 and month_flag=="PROPN"):
									dob_counter=0
									num_counter=0
								else:
									result.add(doc.sentences[j].text)
									date_flag=1
									break
							else:
								result.add(doc.sentences[j].text)
								date_flag=1
								break
						elif "org" in k["ner"].lower():
							wanted_flag=1
							org_flag=1
						elif "gpe" in k["ner"].lower() and (org_flag==1 or loc_flag==1):
							wanted_flag=1
							org_flag=0
							loc_flag=1
						else:
							unwanted_counter+=1
				except:
					pass
		if date_flag!=1 and wanted_flag==1:
			if unwanted_counter<=3:
				result.add(i)
	result_dict={}
	for i in result:
		try:
			j=text.index[i]
			try:
				result_dict[text.index(i)].append(i)
				result_dict[text.index(i)]=sorted(result_dict[text.index(i)], key=lambda x: text.index(i).index(x))
			except:
				result_dict[text.index(i)]=[i]
		except:
			for j in range(len(text)):
				if i in text[j]:
					try:
						result_dict[j].append(i)
						result_dict[j]=sorted(result_dict[j], key=lambda x: text[j].index(x))
					except:
						result_dict[j]=[i]
					break
	payload={"result":[]}
	for i in sorted(result_dict.keys()):
		for j in result_dict[i]:
			payload["result"].append(j)
	return payload