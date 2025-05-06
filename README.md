# BPC-IoT Projekt #8

## Fotopast – Detekce Pohybu

### Popis zařízení

Fotopast je navržena k zachycení fotografií divoké zvěře, která se objeví před fotoaparátem. Předpokládá se umístění v hůře odlehlejších prostorech, proto je potřeba delší životnost napájení. Může se jednat buď o čisté sledování oblasti, nebo může být požadovaným výstupem fotografie splňující náročnější požadavky na estetiku a kvalitu. Náš návrh spočívá primárně v přenosu fotografie na server. Zařízení pojímá SIM kartu, SD kartu a je k němu připojena anténa.

Po detekci pohybu zvěře, která je simulována stiskem tlačítka, se zachytí fotografie, ta se uloží a zaznamená se její index. Poté se přes UDP protokol na server odešle informace o zachycení fotografie. Po odpovědi serveru pak přes TCP protokol odešle v paketech samotnou fotografii. Pokud nelze navázat spojení se serverem, poslání se odkládá o 15 minut, maximálně však o 1 hodinu. Fotografie je tedy uložena jak v zařízení, tak na serveru.

---

## Návrh systému

### Volba přenosové technologie

- **NB-IoT** zvoleno pro zasílání systémových zpráv, jako je zpráva o zachycení obrázku.
- **Cat-M** zvoleno pro zasílání samotného obrázku.

Po odeslání systémové zprávy se prioritně přepne na Cat-M pro odeslání obrazových dat. Pokud není Cat-M k dispozici (timeout), odešle se přes NB-IoT.

- **NB-IoT:** lepší pokrytí a nižší spotřeba
- **Cat-M:** vyšší přenosová rychlost, vhodnější pro obrazová data

### Volba transportního protokolu

- **TCP** – zasílání obrázku (kvůli spolehlivosti)
- **UDP** – zasílání zprávy o záchytu (kvůli úspoře dat)

### Volba aplikačního protokolu

Použit je uměle vytvořený protokol **SIMG**, který sdělí serveru, že přijdou obrazová data. Server odešle zpět zprávu, že hlavičku SIMG přijal (`OK`). Pokud ji nepošle, objeví se chybová hláška.

---

## Zachycení a zpracování obrazu

- **Raspberry Pi Pico** má velmi omezený výkon. Pro práci s obrazem je nutné použít kamerový modul s **JPEG enkodérem**, protože Pico není schopné zpracovat obraz softwarem.
- Tyto kamerové moduly jsou omezené rozlišením a často nemají funkce jako **autofokus (AF)**.
- Alternativa: použití **Raspberry Pi**, které se zapne pouze po detekci pohybu. Pi má větší výkon, podporuje AF, knihovny pro JPEG, a může výstup předat Pico přes např. SPI.

---

## Napájení

- Napájení pomocí **4 AA baterií**, podpořené **solárním napájením**
- Články jako **18650** nejsou vhodné pro spánkový režim
- Zařízení má vyšší nároky na energii kvůli kontinuálnímu vyčítání dat ze senzoru
- Byly použity co nejúspornější součástky a technologie

---

## Popis kódu

### `foto_main`

- Zapnutí modulu pomocí `AT+CFUN=1`
- Kontrola SIM karty: `AT+CPIN?`
- Nastavení pásma, APN, operátora atd.
- Pokud není SIM karta připravena → restart modulu

#### Chování tlačítek:
- **Tlačítko 1** – smaže pořízený obrázek
- **Tlačítko 2** – odešle zprávu o zachycení přes UDP, náhodně zvolí obrázek, uloží ho na SD kartu a odešle pomocí `monitor_radio`

#### Funkce `monitor_radio`
- Naváže TCP spojení
- Pokud úspěšné → pošle obrázek přes `img_send.send_imgv2`
- Pokud neúspěšné → uloží jen na SD
- Kontroluje tlačítko a při stisku spouští `dl_sdcard_comm.comm()`

### `img_send`

- `send_imgv2`: zjistí velikost obrázku, pošle hlavičku, čeká na `OK`, rozdělí obrázek na 512B bloky, odesílá, čeká na `DONE`

### TCP server

- Naslouchá na portu `26903`
- Ukládá obrázky jako `received_image{time_recv}.png`
- Po úspěchu posílá `DONE\n`

---

## Výsledek

Zařízení splňuje očekávanou funkci. Lze připojit fotografický modul, který dodá již zpracovaný JPEG (i v nižším rozlišení). Úspěšně se povedlo odeslat data na server, který je schopen je složit a otevřít.

Byla implementována chybová opatření a fungují správně.

Použité součástky a technologie jsou energeticky úsporné, ale výsledná spotřeba závisí na typu kamerového modulu. Napájení pomocí 4 AA baterií + solární článek bude dále optimalizováno.

---

GitHub repo: [https://github.com/dominik-juze-haus/IoT_CamTrap](https://github.com/dominik-juze-haus/IoT_CamTrap)
