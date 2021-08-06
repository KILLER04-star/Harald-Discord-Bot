Harald ist ein deutscher Discord Bot, welcher die Aufgabe hat, jeden Mittwoch in einem bestimmten Kanal ein "Es ist Mittwoch meine Kerle"-Michmich zu pfostieren.

Funktionen:

    Mittwoch:
    
    "$setzKanal": Mit diesem Befehl wird der Kanal gesetzt, in dem der Mittwoch verkündet wird. 
        Er kann nur von einem Administrator ausgeführt werden.
    "$delkanal" : Mit diesem Befehl wird das senden des Mittwochs abgestellt. 
        Er kann nur von einem Administrator ausgeführt werden.

    "$kanal" : Zeigt an, in welchem Kanal der Mittwoch verkündet wird.
        Dieser Befehl kann von allen Nutzern ausgeführt werden.
    "$bot -mittwoch -fire" : Testet, ob der Mittwoch mit den gegebenen Rechten gesendet werden kann.
        Er kann nur von einem Administrator ausgeführt werden.

    Benötigte Rechte: Nachrichten lesen, Nachrichten schreiben, Dateien anhängen, Nutzer erwähnen, Links einbetten


    Subreddits:
        Der Bot ist in der Lage, Michmichs von Unterlases, wie ich_iel, de, usw. in einen vorgegebenen Kanal des Servers zu pfostieren.
    
        Alle Subreddits:
        -mathmemes
        -physicsmemes
        -aww
        -foodporn
        -wasletztepreis
        -600euro
        -programmerhumor
        -linuxmemes
        -engineeringporn
        -memes
        -me_irl
        -spaceporn
        -badcode
        -electronics
        -electricalengineering
        -dankmemes
        -berstrips
        -okbrudimongo
        -de_EDV
        -HarryPotterMemes
        -Geschichtsmaimais
        -CDU_CSUde
        -CrappyDesign
        -Prequelmemes
        -popular
        -wortwitzkasse
        -techsupportmacgyver

        Momentan ist noch nicht für den Nutzer möglich, eigenständig für den eigenen Server Subreddits auszuwählen.
        Die Memes werden immer um xx:50 Uhr aus mehreren, zufällig aus dieser Liste ausgewählten Subreddits gesendet.

        Benötigte Rechte: Nachrichten lesen, Nachrichten senden, Links einbetten

        Befehle:
        
        "$setz_webhook" : Mit diesem Befehl wird eingestellt, dass in dem Kanal, in dem der Befehl geschrieben wurde, Memes gesendet werden. 
            Dieser Befehl kann nur von einem Administrator ausgeführt werden.
        "$delwebhook" : Mit diesem Befehl werden keine Webhooks mehr gesendet. Er kann in jedem Kanal des Servers ausgeführt werden, in dem der Bot Lese-und Schreibrechte besitzt.
            Dieser Befehl kann nur von einem Administrator ausgeführt werden.
        "$webhook": gibt an, in welchem Kanal die Memes gesendet werden. 
            kann von allen Nutzern ausgeführt werden

    Spiele:
        Der Bot besitzt mehrere Minispiele.

        Kopf oder ZahL:
            "$koz" Mit diesem Befehl wird das Spiel gestartet. Als Argumente können 1 für Zahl, oder 0 für Kopf übergeben werden. Argumente und Befehl müssen durch ein Ausrufezeichen getrennt sein.
            Beispiel: "$koz!1" | "$koz!0" 

        Roulette:
            "$roulette" Mit diesem Befehl wird das Spiel Roulette gestartet. Es können Zahlen zwischen 0 und 36, sowie "s" für Schwarz, oder "r" für Rot eingegeben werden. Befehl und Argument werden auch 
            hier wieder durch ein Ausrufezeichen getrennt.
            Beispiel: "$roulette!1" | "$roulette!s"

        Spiele können von allen Nutzern ausgeführt werden.
        Sie sind kostenlos, es werden keine Gewinne an Spieler ausgezahlt.

        Benötigte Rechte: Nachrichten lesen, Nachrichten schreiben, Dateien anhängen, Links einbetten

    Hilfe: 
        Diese Befehle können von allen Nutzern ausgeführt werden.
        Benötigte Rechte: Nachrichten lesen, Nachrichten schreiben, Links einbetten

        "$help" : Allgemeine Hilfe
        "$help -roulette" : Hilfe zu Roulette
        "$help -koz" : Hilfe zu Kopf oder Zahl
        "$help -webhook" : Hilfe zum Webhook
        "$help -mittwoch" : Hilfe zum Mittwoch
        "$show_commands" : Zeigt eine Liste aller Befehle
        "$private hilfe" : schreibt dem User eine private Nachricht. 
        *Alle Befehle, bis auf die zu den Kanälen und Michmichs, können auch in den DMs ausgeführt werden.

    Andere:
        Diese Befehle können von allen Nutzern ausgeführt werden.
        Benötigte Rechte: Nachrichten lesen, Nachrichten schreiben, Links einbetten
        "$z" : Schreibt irgendein Zitat in den Kanal. 
        "$about" : Zeigt Informationen über den Bot und den Entwickler.
        "$ping" : Zeigt die Latenz des Bots an.

Aufsetzen des Bots auf einem RaspBerry Pi: 

    Software-Anforderungen:
    Python Version 3.7, oder höher
    Cronjob

    Bibliotheken: 
        Asyncio, für das Zeitmanagement
        Sqlite3, für die korrekte Speicherung der Daten (Serverids und Channelids)
        Praw, für die Reddit-Anbindung
        Discord.py für die Verwendung von Discord-Funktionen
        Discord_slash für die Verwendung von Discord Slash Commands
    
    Es wird empfohlen, pip für die Installation der Bibliotheken zu verwenden.

Versteckte Ordner und Dateien: 
    Aufgrund der Sicherheit wurden einige Dateien und Ordner nicht in die Versionskontrolle eingebunden.
    Dazu zählen:
    Ordner: log
    Dateien im Ordner: "errorlog.txt" | Eine Datei, in die der Bot alle Laufzeitfehler einschließlich Zeit-und Datumsstempel schreibt.
    Ordner: private
    Dateien:
    author.txt : Die Datei enthält den Namen und Diskriminator des Discord-Accounts des Programmierers.
    keys.txt: Die Datei enthält das Bot-Token.
    praw.ini: Die Datei enthält sämtliche Reddit-Keys.
    Info.db: Datenbankdatei für die Selbstverwaltung des Bots.

Datenbankstruktur:
Tabellen:
Info:
enthält server_id (primary key) und channel_id eines Servers für das Senden des Mittwoch-Maimais
Status
enthält server_id (primary key), Status des Mittwoch-Maimais und Notizen (z.B.: Fehler beim Senden, letzte Sendezeit)
Webhook-Channels 
enthält server_id (primary key) und channel_id eines Servers für das Senden von anderen Maimais
sub_names
eine Liste aller Subreddits für das Senden der anderen Maimais

Der Pi sollte alle 24h einmal neu gestartet werden (Cronjob eignet sich hierfür).
Um den Bot automatisch zu starten folgende Befehle ausführen:

sudo nano /etc/profile

Jetzt öffnet sich ein Editor.
Bis zum Ende der Datei Scrollen und folgenden Code hinzufügen:

sleep 60    | 60 Sekunden warten, bis sich der Pi mit dem Netzwerk verbunden hat.
cd "Pfad_zu_meiner_main_bot.py_Datei"
sudo python3 main_bot.py &

Dem & Zeichen kommt hier eine besondere Bedeutung zu. Es ist also essenziell wichtig, dass es dort steht.
Es sorgt nämlich dafür, dass der Bot im Hintergrund ausgeführt wird, denn wenn dies nicht passiert und der Bot im Vordergrund ausgeführt wird,
führt dies dazu, dass der Pi seinen Bootvorgang nicht fortsetzt und dadurch UNBENUTZBAR wird.

Für Fragen gerne auf GitHub bei mir melden :)