brace per la qualità dell'aria nelle città italiane
===================================================

- Elaborazione dei dati ISPRA

La prima fase del processo consiste nell'elaborazione dei dati
pubblici sulla qualità dell'aria nelle principali città sul territorio
italiano, messi a disposizione dall'ISPRA (Istituto Superiore per la
Protezione e la Ricerca Ambientale). Per poter effettuare
l'elaborazione è stato realizzato un tool a riga di comando, brace.

Il tool, rilasciato sotto licenza GPL, è presente sulla piattaforma di
Social Coding github all'indirizzo:

https://github.com/mwolf76/brace

Chiunque fosse interessato può analizzare, modificare e ripubblicare
il codice sorgente, adattandolo a esigenze sue o di terzi.

Il tool è dotato di documentazione in linea, richiamabile mediante
l'opzione --help.  Digitando il seguente comando al prompt della riga
di comando:

$ brace.py --help

Verrà visualizzato il seguente messaggio:

--------------------------------------------------------------------------------
brace.py - a tool for public data knowledge sharing.

usage:

    brace.py [ --from=<from_year> ][ --to=<to_year> ]
             --region=<region> --pollutant=<formula>
             [ --help ] [ --verbosity=<level> ]
             filename

options:

  --from=<from_year>, determines the starting year for the analysis
  (e.g. 2003). If not specified the earliest year for which data is
  available is picked. (currently this is 2002).

  --to=<to_year>, determines the ending year for the analysis
  (e.g. 2003). If not specified the latest year for which data is
  available is picked. (currently this is 2009).

  --region=<region>, (case-insensitive) determines which localized
  data set is to be processed. This is a mandatory argument.  If not
  specified, the list of italian regions is displayed. If specified
  more than once, output is produced for all of the given regions.

  --pollutant=<formula>, (case-insensitive) determines which pollutant
  data set is to be processed. This is a mandatory argument. If not
  specified, the list of known pollutants is displayed. If specified
  more than once, output is produced for all of the given pollutants.

  --help, prints this message.

  --verbosity=<level>, adjusts the level of verbosity of the
  tool. This is a number between 0(quiet) and 3(extremely
  verbose). This is manly for debugging purposes.

arguments:

  filename, the filename to write the output to.
--------------------------------------------------------------------------------

Questo messaggio elenca le opzioni disponibili per modificare il
comportamento del tool. Nota: Le opzioni mostrate tra parentesi quadre
(e.g. verbosity) sono facoltative. Se non indicate, il tool sceglierà
un valore di default "ragionevole" e proseguirà l'elaborazione senza
mostrare messaggi d'errore.

A titolo esemplificativo mostriamo come effettuare l'elaborazione dei
dati sull'inquinamento da Anidride Solforosa (NO2) in Lombardia negli
anni dal 2005 al 2008. L'utilizzo del formato DSPL (Dataset Publishing
Language) costituisce un requisito necessario per la visualizzazione
sulla piattaforma Google Public Data Explorer. È tuttavia possibile
utlizzare altri formati

$ ./brace.py --from=2005 --to=2008 --region=Lombardia --pollutant=NO2 --format=DSPL 

- Upload dei dati su Google Public Data Explorer

Il comando precedente genera un Dataset in formato DSPL. Il passo
successivo consiste nell'upload del dataset così ottenuto sui server
di Google (è necessario un account Google per effettuare questa
operazione).

- Visualizzazione dei grafici

Una effettuato l'upload dei dati sulla piattaforma fornita da Google,
è possibile impostare il tipo di visualizzazione e alcuni parametri.


