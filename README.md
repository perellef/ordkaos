# Ordmester – kjapp gloselæring, null fiksfakseri

Lei språkapper du bruker 1 time på å kun lære 10 ord? Da bør du prøve **Ordmester**. Ordmester er en app som nærmest lar deg *speedrunne* nye ord.

Ordmester er strippet for alt visvas gloselæring ikke trenger.

## Kom i gang

1. Installer avhengigheter.
```bash
pip install -r requirements.txt
```

2. Velg om du vil lagre glosene dine i et Excelark, et Google-regneark eller begge deler.
   - **excelark**:
        1. Kopier alle filer i `maler` til `mine-gloser`. Kjør `python kode/hovedprogram.py` for å se at alt er satt opp riktig.

   - **Google-regneark**: 
        1. Skaff Google-credentials:
            1. [Velg et eksisterende eller opprett et Google Cloud Project](https://console.cloud.google.com/iam-admin/serviceaccounts)
            2. Under [service accounts](https://console.cloud.google.com/iam-admin/serviceaccount) velg en eksisterende eller opprett en servicebruker: `Create service account`.
               - Ved opprettelse av ny servicebruker må du [gi den rettigheter til å redigere Google-regneark](https://console.cloud.google.com/iam-admin/iam).
            3. Under service accounten naviger til `Keys`, og opprett ny nøkkel: `Add key`. Du skal nå ha fått lastet ned en json.fil med credentials. Sørg for å holde disse hemmelig.
        2. Opprett en .env-fil i prosjektmappen og fyll inn:
        
            ```
            GOOGLE_PROJECT_ID=
            GOOGLE_PRIVATE_KEY_ID=
            GOOGLE_PRIVATE_KEY=
            GOOGLE_CLIENT_EMAIL=
            GOOGLE_CLIENT_ID=
            ```
        3. Opprett et Google-ark.
           - Legg til service-brukeren: `DEL` og skriv inn klient-emailen.
           - Lag en ny fane med navn `Ordliste`.
           - Kopier over innholdet fra `maler/Mal.xlsx`->`Ordliste` til Google-arket->`Ordliste`.
           - Hent ut `Regneark-ID` fra URL-en `https://docs.google.com/spreadsheets/d/REGNEARK-ID`.
        4. Kopier over `ordark.json` og `kategorier.json` i `maler` til `mine-gloser`.
            - I `ordark.json`:
                - sett `fil-id: "<Regneark-ID>"`
                - sett `les-fra: true` og `les-til: true` for `googleark`. 
                - hvis ikke excelark: sett `les-fra: false` og `les-til: false` for `excelark`. 
        5. Kjør `python kode/hovedprogram.py` og sjekk at alt er satt opp korrekt.

