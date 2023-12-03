# Keskustelusovellus
Sovelluksessa on kaikki ominaisuudet mitä foorumilta tai keskustelupalstalta olettaa. Käyttäjät voivat aloittaa keskusteluketjuja ja lisätä viestejä niihin ylläpitäjien ylläpitämillä keskustelualueilla. Sovellus ei ainakaan vielä ole testattavissa fly.iossa.
### Käynnistysohjeet
Toimii aika malliohjeiden mukaisesti. Lataa repositorio ja luo ensin juurikansioon seuraavanlainen **.env** 


    DATABASE_URL=<tietokannan-paikallinen-osoite>
    SECRET_KEY=<salainen-avain>
    OWNER=<käyttäjänimi>


OWNER on siis ainoa käyttäjä joka kykenee adminien lisäämiseen ja poistamiseen, jos näitä ei halua testata niin ei ole pakko määrittää. Sitten alustetaan samalla tavalla virtuaaliympäristö ja riippuvuudet

    python3 -m venv venv
    source venv/bin/activate
    pip install -r ./requirements.txt

Samoin schema.sql. *HUOM!* schema.sql poistaa käyttämänsä nimisiä taulukoita jos niitä löytää, jos tietokannassa on tärkeitä taulukoita niin kannattaa tallentaa ne ensin tai jtn. **Varmista** myös että tietokanta on avattu, tuon komennon psql täytyy toimia normaalisti (Jos postgresql asennu oli scriptillä niin start-pg.sh käynnistää).

    psql < schema.sql

Sovelluksen voi nyt käynnistää

    flask run

Schema.sql myös luo kaksi käyttäjää jo valmiiksi testaamista varten, "user" ja "admin", molemmilla salasanana "1234".

### Sovelluksen ominaisuudet (Tällä hetkellä)
- Käyttäjä näkee alkusivulla keskustelualueet 
- Käyttäjä voi myös alkusivulla kirjautua sisään tai jatkaa ilman
- Ilman kirjautumista viestejä voi silti lukea, mutta niitä ei voi lisätä
- Käyttäjä voi keskustelualueilla aloittaa viestillä uuden ketjun
- Käyttäjä voi myös lisätä viestinsä jo valmiiksi olemassa olevan ketjun jatkeeksi
- Käyttäjä voi poistaa lähettämiään viestejä
- Käyttäjä voi etsiä ketjuja ja viestejä niiden sisältämän tekstin pohjalta
- Käyttäjä voi vaihtaa salasanaa ja poistaa käyttäjätilin
- Käyttäjä voi lisätä muista kavereiksi ja sitten lähettää suoraan viestejä
    - Direct messaged siis näkyvät vain kahdelle käyttäjälle jotka on lisännyt toisensa kaveriksi
- Ylläpitäjä voi lisätä keskustelualueita ja poistaa alueita, ketjuja ja viestejä
- Omistaja voi määrätä käyttäjien adminoikeuksia.
### Suuret puuttuvuudet
- Ulkoasu, sivu näyttää aika huonolta vielä
- directmessage haku ei toimi jostain syystä
- Kattavampi testaus, kaiken **pitäisi** toimia, mutta silti
### Mahdollisia lisäyksiä (ei todennäköisesti enään projektin aikana kerkeä)
- Monia mukavuuksia, mm.
    - viestien muokkaaminen, uuden kirkoittamisen sijaan
    - kaverikutsujen rajoittaminen, spammin välttämiseen
    - samasta syystä käyttäjän estäminen sovelluksesta
    - salasanan laaduntarkastus, hetkellä esim. yksi kirjain kelpaa
- Rajoitetut alueet/ketjut, joihin vain määrätyt käyttäjät pääsevät 
    - Voi vielä erotella suljetut ja peitetyt, missä siis suljettuihin ei pääse ilman kutsua ja peitettyjä ei edes näe ilman
    - Näihin täytyy sitten oletettavasti pystyä lisäämään ja poistamaan jäseniä
    - Rajoitetuille ketjuille täytyy olla ketjun omat ylläpitäjät.
    - Mahdollisesti ennen lisäämistä lähetettyjä viestejä ei näe
- Kuvien lähettäminen, tosin tämä on prioriteettilistan perällä
