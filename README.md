🏙️ Vilniaus Istorijos Paieškos Asistentas
Interaktyvus klausimų-atsakymų asistentas, leidžiantis ieškoti informacijos apie Vilniaus miestą ir jo istoriją, naudojant įvairius šaltinius – Wikipedia, tekstinius failus ir (galimai) YouTube transkriptus. Sukurtas naudojant LangChain ir RAG (Retrieval-Augmented Generation) principą.

🔧 Naudojamos technologijos
🧠 LangChain – dokumentų analizė ir integravimas

🤖 OpenAI GPT per Azure (arba GitHub inference endpoint)

🗂️ TextLoader / WebBaseLoader – skirtingų šaltinių įkėlimas

💬 Streamlit – grafinė naudotojo sąsaja

🧠 InMemoryVectorStore – laikina vektorinė saugykla

📄 Wikipedia ir info.txt failas kaip duomenų šaltiniai

📦 Projekto struktūra
bash
Kopijuoti
Redaguoti
AI_agent_demo/
├── demo.py              # Pagrindinis aplikacijos failas
├── info.txt             # Papildomas tekstinis šaltinis
├── .env                 # Slaptas raktas (API)
├── requirements.txt     # Reikalingų paketų sąrašas
└── README.md            # Aprašas (šis failas)
🚀 Paleidimas
Klonuok arba parsisiųsk šį projektą.

Įdiek reikiamas priklausomybes:

bash
Kopijuoti
Redaguoti
pip install -r requirements.txt
Sukurk .env failą ir įrašyk savo OpenAI raktą:

env
Kopijuoti
Redaguoti
SECRET=your_openai_or_azure_api_key
Paleisk aplikaciją:

bash
Kopijuoti
Redaguoti
streamlit run demo.py
📝 Naudojimas
Įrašyk klausimą apie Vilnių (pvz.: "Kada Vilnius tapo sostine?").

Aplikacija ieško atsakymo įvairiuose šaltiniuose (Wikipedia, info.txt).

Rezultatas bus pateiktas su naudotų šaltinių sąrašu.

📚 Duomenų šaltiniai
Wikipedia – Vilnius

Wikipedia – Vilniaus istorija

info.txt – papildomas tekstinis dokumentas

⚠️ Pastabos
RAG modelis naudoja OpenAIEmbeddings, todėl būtinas API raktas.

Gali būti taikomi kvotų (rate limit) apribojimai.

YouTube transkriptų įkėlimas kol kas yra išjungtas dėl API apribojimų.

✅ Ateities planai
✅ Integruoti YouTube transkriptus

✅ Vizualizuoti atsakymus žemėlapyje (koordinatės)

⏳ Išplėsti su daugiau vietinių šaltinių (PDF, docx)

👩‍💻 Autorius
Projektas sukurtas kaip eksperimentinis įrankis Vilniaus istorijos pažinimui naudojant dirbtinį intelektą.
