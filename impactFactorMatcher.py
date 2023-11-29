import pandas as pd
import camelot
from pprint import pprint
import re
import openpyxl
from matplotlib import pyplot as plt
from thefuzz import fuzz
import numpy as np

def firstInName(string):
	stringBuilder = ""
	for name in string.split(" "):
		stringBuilder += name[0]
	return stringBuilder

authorList = [
	"Løes IM",
	"Lønning PE",
	"Knappskog S",
	"Eikesdal HP",
	"Pettersen HES",
	"Hestetun KE",
	"Dahl O",
	"Myklebust MP",
	"Fluge Ø",
	"Boer CG",
	"Fjellanger K",
	"Sandvik IM",
	"Ugland M",
	"Engeseth GM",
	"Hysing LB",
	"Sorbye H",
	"Bolstad K",
	"Samnøy AT",
	"Stokkevåg CH",
	"Sulen TH",
	"Handeland AH",
	"Kvåle R",
	"Kjellstadli C",
	"Kvåle R",
	"Dahle TJ",
	"Hjelle Å",
	"Jebsen NL",
	"Karlsdóttir Á",
	"Mella O",
	"Rosenlund NB",
	"Stanisavljevic L",
	"Venizelos A",
	"Frøystein T",
	"Brekke J",
	"Nikolaienko O",
	"Straume K",
	"Goplen D",
	"Ranes M",
	"Wiestad TH",
	"Thormodsen I",
	"Arving C",
	"Rekeland IG",
	"Sørland K",
	"Risa K",
	"Alme K",
	"Heggdal J",
	"Sofiyeva N",
	"Gansmo LB",
	"Sommerfelt H",
	"Dillekås H",
	"Straume O",
	"Engebrethsen C",
	"Deng W",
	"Geisler J",
	"Inversen GT",
	"Aasebø K"
]

authorList = [k.lower() for k in authorList]

adHocList = { # not found elsewhere, this list was complied from the journals' official sites 
	"Journal of Clinical Psychology": 3,
	"Advances in Urology": 1.4,
	"Journal of Physiology": 5.5,
	"Journal of Vocational Rehabilitation": 0.409,
	"European Radiology Experimental": 3.8,
	"Journal of Addictive  Diseases": 2.3,
	"European Cardiology": 3.0,
	"International Journal of Mental Health Systems": 3.6,
	"Scandinavian Journal of Psychology": 2.1,
	"Frontiers in Psychology": 3.8,
	"Inspira- Journal of Anesthesia, Operating Room and Critical Care Nursing": np.nan,
	"Open heart": 2.7,
	"Den norske tannlegeforenings tidende": np.nan,
	"Sykepleien Forskning": np.nan,
	"ASAIO journal (1992)": 4.2,
	"Spinal Cord Series and Cases": 1.2,
	"Oxford Medical Case Reports": 0.5,
	"European Heart Journal - Case Reports": 1,
	"Social Policy & Administration": 3.2,
	"BMC Pilot and Feasibility Studies": 1.7,
	"Journal of Experimental Orthopaedics": 1.8,
	"Neurology Research International": 1.5,
	"Biomedical Engineering & Physics Express": 1.4,
	"Springer": np.nan,
	"Viruses": 4.7,
	"BMJ Open Quality": 1.4,
	"Journal of Mental Health": 6.33,
	"Journal of ISAKOS: Joint Disorders & Orthapaedic Sports Medicine": 1.6,
	"Stress": 3.493,
	"Journal of Clinical Urology (JCU)": 0.3,
	"BMJ Case Reports": np.nan,
	"Nordic journal of music therapy": 1.6,
	"Ultrasound International Open": 3.2,
	"International Journal of Cardiology: Cardiovascular Risk and Prevention (IJCCRP)": 2.3,
	"Obesity Science & Practice": 2.2,
	"Lecture Notes in Computer Science (LNCS)": 0.407,
	"Biomarker Insights": 3.8,
	"Canadian Journal of Anesthesia": 4.2,
	"Head and Neck": 2.9,
	"European Journal of Surgical Oncology": 3.8,
	"Nuklearmedizin": 2.22,
	"Case Reports in Immunology": 1,
	"Radiography": 2.6,
	"Physiotherapy Research International": 1.7,
	"Innovations in Systems and Software Engineering": 1.1,
	"Ophthalmology Retina": 4.5,
	"Behaviour Research and Therapy": 5.321,
	"Frontiers in Digital Health": 2.3,
	"Death Studies": 3.8,
	"American Society of Nephrology. Clinical Journal": 9.8,
	"Nevropsykologi : Medlemsblad for Norsk Nevropsykologisk Forening": np.nan,
	"Oxidative Medicine and Cellular Longevity": 7.3,
	"Urologic Oncology": 2.7,
	"Thrombosis Update": 0.9,
	"Clinical Obesity": 3.3,
	"BJPsych International": 1.65,
	"Nordic Journal of Studies in Policing (NJSP)": 0.182,
	"": np.nan,
	"Medicina": 2.6,
	"Clinical and Experimental Dental Research": 1.8,
	"International Journal of Law and Psychiatry": 2.3,
	"Clinical Neurophysiology Practice": 1.7,
	"Tidsskrift for Den norske legeforening": 0.29,
	"International Journal of Neonatal Screening (IJNS)": 3.5,
	"Emotion": 4.2,
	"Journal of Imaging": 3.2,
	"Journal of Personalized Medicine": 3.4,
	"Community mental health journal": 2.6,
	"European Burn Journal": np.nan,
	"Neuro-Oncology Advances (NOA)": 3.5,
	"Counselling and Psychotherapy Research": 2.4,
	"Cancer Treatment and Research Communications": 0.52,
	"Assessment (ASM)": 3.8,
	"Communications Medicine": np.nan,
	"Addictive Behaviors Reports": 4.024,
	"Plants": 4.5,
	"JMIR Research Protocols": 1.7,
	"JBMR Plus": 3.8,
	"JBJS Open Access": np.nan,
	"Gazzetta Medica Italiana": 0.1,
	"Substance Abuse: Research and Treatment": 2.1,
	"Body image": 5.2,
	"Nordic Psychology": 1.2,
	"Advances in Sample Preparation": np.nan,
	"Research in Psychotherapy: Psychopathology, Process and Outcome": 2.7,
	"PLOS Global Public Health": np.nan,
	"International journal of cardiology: Heart and Vasculature (IJCHA)": 2.9,
	"International Journal of Qualitative Studies on Health and Well-being": 1.8,
	"European Heart Journal Open (EHJ Open)": np.nan,
	"Psychology of Addictive Behaviors": 3.4,
	"European Clinical Respiratory Journal": 1.9,
	"JMIR Formative Research": 2.2,
	"Internet Interventions": 4.3,
	"Neuro-Oncology Practice": 2.7,
	"NPJ Parkinson's Disease": 8.7,
	"Ergoterapeuten": np.nan,
	"Personality Disorders: Theory, Research, and Treatment": 2.8,
	"Eurographics Workshop on Visual Computing for Biomedicine": np.nan,
	"Osteoarthritis and Cartilage Open": np.nan,
	"High Blood Pressure & Cardiovascular Prevention": 2.4,
	"Journal of the Intensive Care Society (JICS)": 2.7,
	"Crime, Media, Culture: An International Journal": 1.8,
	"BMC Psychology": 3.6,
	"International Journal of Environmental Research and Public Health": np.nan,
	"European Journal of Radiology Open (EJR Open)": 2,
	"Clinical Psychology": 3,
	"Law and Human Behavior": 2.5,
	"Journal of Psychosocial Rehabilitation and Mental Health": np.nan
}

filename = "NVI - 1936 HAUKELAND 2022.xlsx"
filename2 = "Ekstra fra kreftavd.xlsx"


def getListOfJournals() -> set:
	df = pd.read_excel(filename, engine="openpyxl")

	df["NAVN"] = df.ETTERNAVN + " " + df.FORNAVN.map(firstInName)
	df = df.drop_duplicates(subset="VA_TITTEL")
	journals = df.PUBLISERINGSKANALNAVN

	df["Kreftavd"] = 0

	df2 = pd.read_excel(filename2, engine="openpyxl")
	# Check of any of df2.Title is not in df.VA_TITTEL

	oncologyJournalsList = list()

	with open("oncologyJournals.csv", "r") as oncologyJournals:
		for line in oncologyJournals.readlines():
			oncologyJournalsList.append(line[:-1].lower())

	yes = 0
	no = 0

	jset = set()

	for index, row in df.iterrows():
		journal = row["PUBLISERINGSKANALNAVN"]
		name = row["VA_TITTEL"]
		authorname = row["NAVN"]
		if journal.lower() in oncologyJournalsList:
			yes += 1
			df.at[index, "Kreftavd"] = 1
			jset.add(name)
		else:
			if "cancer" in journal.lower() or "oncol" in journal.lower() or "radiotherapy" in journal.lower() or "chemotherapy" in journal.lower():
				yes += 1
				df.at[index, "Kreftavd"] = 1
				jset.add(name)
			elif "cancer" in name.lower() or "oncol" in name.lower() or "radiotherapy" in name.lower() or "chemotherapy" in name.lower():
				yes += 1
				df.at[index, "Kreftavd"] = 1
				jset.add(name)
			elif authorname.lower() in authorList:
				yes += 1
				df.at[index, "Kreftavd"] = 1
				jset.add(name)
			else:
				no += 1

	to_df = {"EIERKODE": list(),
				"ARSTALL_REG": list(),
				"ISSN": list(),
				"KVALITETSNIVAKODE": list(),
				"ETTERNAVN": list(),
				"FORNAVN": list(),
				"PUBLISERINGSKANALNAVN": list(),
				"UTBREDELSESOMRADE": list(),
				"SIDE_FRA": list(),
				"SIDE_TIL": list(),
				"SIDEANTALL": list(),
				"VA_TITTEL": list(),
				"SPRÅK": list(),
				"Kreftavd": list()
	}

	for index, row in df2.iterrows():
		_ , score = fuzzyMatch(row["Title"], list(df["VA_TITTEL"]))
		if score < 80: # No matches found, add this new item
			yes += 1
			print("Added ", row["Title"])
			to_df["EIERKODE"].append("HBE")
			to_df["ARSTALL_REG"].append("2022")
			to_df["ISSN"].append("")
			to_df["KVALITETSNIVAKODE"].append("1")
			to_df["ETTERNAVN"].append(row["Authors"])
			to_df["FORNAVN"].append("")
			to_df["PUBLISERINGSKANALNAVN"].append(row["Journal"])
			to_df["UTBREDELSESOMRADE"].append("")
			to_df["SIDE_FRA"].append("")
			to_df["SIDE_TIL"].append("")
			to_df["SIDEANTALL"].append("")
			to_df["VA_TITTEL"].append(row["Title"])
			to_df["SPRÅK"].append("Engelsk")
			to_df["Kreftavd"].append(1)

	df3 = pd.concat([df, pd.DataFrame(to_df)], ignore_index=True)

	print("included: ", yes, ", not included: ", no)
	return df3

def loadImpactFactor() -> dict:
	impactFactor = dict()

	with open("impactFactor.csv") as file:
		for line in file.readlines():
			parsed = line.split(";")
			num = parsed[2]
			idx = parsed[0]
			
			if "P" in num:
				numfloat = float(num[1:])
			elif "S" in num and len(num)>2:
				numfloat = float(num[2:])
			elif "S" in num and len(num) == 2:
				numfloat = float(num[1:])
			elif "N" in num:
				numfloat = float(num[1:])
			elif "R" in num:
				numfloat = float(parsed[3])
			elif num == "":
				numfloat = float(parsed[3])
			elif parsed[0] == "5073":
				numfloat = 2.5
			elif parsed[0] == ' & C"':
				continue
			elif parsed[0] == "5271":
				numfloat = float(num[1:])
			elif parsed[0] == "5272":
				numfloat = 2.4
			elif parsed[0] == '2.4"':
				continue
			elif idx == "5846":
				numfloat = 2.1
			elif idx == "6002":
				numfloat = 2
			elif idx == "6073":
				numfloat = 2
			elif idx == "6534":
				numfloat = 1.8
			elif idx == "6609":
				numfloat = 1.7
			elif idx == "7012":
				numfloat = 1.6
			elif idx == ' E"':
				continue
			elif idx == "7393":
				numfloat = 1.4
			elif idx == '1.4"':
				continue
			elif idx == '8710':
				numfloat = 0.7
			elif idx == '9427':
				numfloat = 0.2
			elif idx == '9484':
				break
			else:
				numfloat = float(num)

			impactFactor[parsed[1].lower().strip()] = float(numfloat)

	df2 = pd.read_excel(filename2, engine="openpyxl")
	for index, row in df2.iterrows():
		if not pd.isna(row['ImpactFactor']):
			impactFactor[row["Journal"]] = float(row['ImpactFactor'])
			print(impactFactor[row["Journal"]])

	return impactFactor

def matchJournalsToImpactFactor(df: pd.DataFrame) -> dict:

	journals = set(df.PUBLISERINGSKANALNAVN)

	impactFactor = loadImpactFactor()
	res = dict()
	yes = 0
	manual = 0
	fuzzy = 0

	for journal in journals:
		if journal.lower() in impactFactor:
			res[journal] = impactFactor[journal.lower()]
			yes += 1
		else:
			if journal in adHocList:
				res[journal] = adHocList[journal]
				manual += 1
			else:
				highestMatch, _ = fuzzyMatch(journal, impactFactor)
				fuzzy += 1
				if highestMatch:
					res[journal] = impactFactor[highestMatch]

	tot = yes + manual + fuzzy
	print("yes: ", yes/tot, "manual: ", manual/tot, "fuzzy: ", fuzzy/tot)
	return res

def fuzzyMatch(string: str, listOfStrings: list):
	bestScore = 0
	bestItem = None
	for item in listOfStrings:
		simScore = fuzz.ratio(string.lower(), item.lower())
		if simScore > bestScore:
			bestScore = simScore
			bestItem = item

	return bestItem, bestScore

def addImpactFactorToExcel(impactFactorMap):
	df["Impact Factor"] = df["PUBLISERINGSKANALNAVN"].map(impactFactorMap)
	df.to_excel("Output with impact factor and extra publications.xlsx")

if __name__ == "__main__":
	df = getListOfJournals()
	impactFactorMap = matchJournalsToImpactFactor(df)
	addImpactFactorToExcel(impactFactorMap)