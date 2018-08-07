# HOMEINFO News API

Bei der HOMEINFO News API (HINEWS) handelt es sich um eine ReST basierte
Webanwendung, welche von HOMEINFO verfasste Nachrichten anbietet.

## Public API

Um außerhalb der HOMEINFO Systeme auf die entsprechenden Nachrichten zugreifen
zu können, muss die *public API* verwendet werden. Diese findet sich unter der
URL `https://backend.homeinfo.de/hinews/pub` und stellt folgende Endpoints
bereit:

1. `GET /article`                 Listet vorhandene Artikel auf.
2. `GET /article/<int:ident>`     Gibt den angegebenen Artikel zurück.
3. `GET /image/<int:ident>`       Gibt den angegebenen Anhang zurück.

Zur Authentifizierung des entsprechenden Kunden muss des Weiteren unbedingt das
Berechtigungstoken über den URL Parameter `access_token=<token>` angegeben
werden.

**Hinweis:** Da dieses Token geheim ist, darf es nicht außerhalb eines
authentifizierten Kontexts in Ajax Calls verwendet werden.

### Auflistung

Die Auflistung der Artikel gibt eine Liste folgender Objekte zurück:

    {
      "$id": "http://example.com/example.json",
      "type": "object",
      "definitions": {},
      "$schema": "http://json-schema.org/draft-07/schema#",
      "properties": {
        "created": {
          "$id": "/properties/created",
          "type": "string",
          "title": "The Created Schema ",
          "default": "",
          "examples": [
            "2018-07-30T09:29:56"
          ]
        },
        "title": {
          "$id": "/properties/title",
          "type": "string",
          "title": "The Title Schema ",
          "default": "",
          "examples": [
            "Ernteausfälle durch Dauerhitze"
          ]
        },
        "id": {
          "$id": "/properties/id",
          "type": "integer",
          "title": "The Id Schema ",
          "default": 0,
          "examples": [
            270
          ]
        },
        "source": {
          "$id": "/properties/source",
          "type": "string",
          "title": "The Source Schema ",
          "default": "",
          "examples": [
            "http://www.tagesschau.de/inland/hitze-kartoffeln-101.html"
          ]
        },
        "customers": {
          "$id": "/properties/customers",
          "type": "array"
        },
        "active_from": {
          "$id": "/properties/active_from",
          "type": "string",
          "title": "The Active_from Schema ",
          "default": "",
          "examples": [
            "2018-07-30"
          ]
        },
        "tags": {
          "$id": "/properties/tags",
          "type": "array"
        },
        "text": {
          "$id": "/properties/text",
          "type": "string",
          "title": "The Text Schema ",
          "default": "",
          "examples": [
            "Aufgrund der Dauerhitze in Deutschland kommt es vermehrt zu Ernteausfällen von bis zu 40 Prozent. Auch Kartoffeln sind betroffen. Da die Kartoffeln bei der Hitze ihr Wachstum einstellen, sind die Knollen nur sehr klein. Besonders die Pommes Frites Produktion leidet darunter. So werden die nächsten Pommes Frites wohl kurz ausfallen. Daher könnten künftig Preissteigerungen zu erwarten sein, damit die Missernten finanziell wieder eingebracht werden. Auf Importe aus Nicht-EU-Ländern soll aber wegen hohen Transportkosten und Kartoffelkrankheiten verzichtet werden."
          ]
        },
        "active_until": {
          "$id": "/properties/active_until",
          "type": "string",
          "title": "The Active_until Schema ",
          "default": "",
          "examples": [
            "2018-08-07"
          ]
        },
        "images": {
          "$id": "/properties/images",
          "type": "array",
          "items": {
            "$id": "/properties/images/items",
            "type": "object",
            "properties": {
              "uploaded": {
                "$id": "/properties/images/items/properties/uploaded",
                "type": "string",
                "title": "The Uploaded Schema ",
                "default": "",
                "examples": [
                  "2018-07-30T09:29:57"
                ]
              },
              "id": {
                "$id": "/properties/images/items/properties/id",
                "type": "integer",
                "title": "The Id Schema ",
                "default": 0,
                "examples": [
                  339
                ]
              },
              "mimetype": {
                "$id": "/properties/images/items/properties/mimetype",
                "type": "string",
                "title": "The Mimetype Schema ",
                "default": "",
                "examples": [
                  "image/jpeg"
                ]
              },
              "source": {
                "$id": "/properties/images/items/properties/source",
                "type": "string",
                "title": "The Source Schema ",
                "default": "",
                "examples": [
                  "https://pixabay.com/de/kartoffeln-gem%C3%BCse-erdfrucht-bio-1585060/"
                ]
              }
            }
          }
        }
      }
    }

### Einzelner Artikel

Die Abfrage eines einzelnen Artikels liefert folgende Rückgabe:

    {
      "$id": "http://example.com/example.json",
      "type": "object",
      "definitions": {},
      "$schema": "http://json-schema.org/draft-07/schema#",
      "properties": {
        "created": {
          "$id": "/properties/created",
          "type": "string",
          "title": "The Created Schema ",
          "default": "",
          "examples": [
            "2018-07-30T09:29:56"
          ]
        },
        "title": {
          "$id": "/properties/title",
          "type": "string",
          "title": "The Title Schema ",
          "default": "",
          "examples": [
            "Ernteausfälle durch Dauerhitze"
          ]
        },
        "id": {
          "$id": "/properties/id",
          "type": "integer",
          "title": "The Id Schema ",
          "default": 0,
          "examples": [
            270
          ]
        },
        "source": {
          "$id": "/properties/source",
          "type": "string",
          "title": "The Source Schema ",
          "default": "",
          "examples": [
            "http://www.tagesschau.de/inland/hitze-kartoffeln-101.html"
          ]
        },
        "customers": {
          "$id": "/properties/customers",
          "type": "array"
        },
        "active_from": {
          "$id": "/properties/active_from",
          "type": "string",
          "title": "The Active_from Schema ",
          "default": "",
          "examples": [
            "2018-07-30"
          ]
        },
        "tags": {
          "$id": "/properties/tags",
          "type": "array"
        },
        "text": {
          "$id": "/properties/text",
          "type": "string",
          "title": "The Text Schema ",
          "default": "",
          "examples": [
            "Aufgrund der Dauerhitze in Deutschland kommt es vermehrt zu Ernteausfällen von bis zu 40 Prozent. Auch Kartoffeln sind betroffen. Da die Kartoffeln bei der Hitze ihr Wachstum einstellen, sind die Knollen nur sehr klein. Besonders die Pommes Frites Produktion leidet darunter. So werden die nächsten Pommes Frites wohl kurz ausfallen. Daher könnten künftig Preissteigerungen zu erwarten sein, damit die Missernten finanziell wieder eingebracht werden. Auf Importe aus Nicht-EU-Ländern soll aber wegen hohen Transportkosten und Kartoffelkrankheiten verzichtet werden."
          ]
        },
        "active_until": {
          "$id": "/properties/active_until",
          "type": "string",
          "title": "The Active_until Schema ",
          "default": "",
          "examples": [
            "2018-08-07"
          ]
        },
        "images": {
          "$id": "/properties/images",
          "type": "array",
          "items": {
            "$id": "/properties/images/items",
            "type": "object",
            "properties": {
              "uploaded": {
                "$id": "/properties/images/items/properties/uploaded",
                "type": "string",
                "title": "The Uploaded Schema ",
                "default": "",
                "examples": [
                  "2018-07-30T09:29:57"
                ]
              },
              "id": {
                "$id": "/properties/images/items/properties/id",
                "type": "integer",
                "title": "The Id Schema ",
                "default": 0,
                "examples": [
                  339
                ]
              },
              "mimetype": {
                "$id": "/properties/images/items/properties/mimetype",
                "type": "string",
                "title": "The Mimetype Schema ",
                "default": "",
                "examples": [
                  "image/jpeg"
                ]
              },
              "source": {
                "$id": "/properties/images/items/properties/source",
                "type": "string",
                "title": "The Source Schema ",
                "default": "",
                "examples": [
                  "https://pixabay.com/de/kartoffeln-gem%C3%BCse-erdfrucht-bio-1585060/"
                ]
              }
            }
          }
        }
      }
    }

### Bilder
Die Abfrage der Bilder liefert diese als Binärdaten mit dem entsprechenden
*ContentType* zurück.