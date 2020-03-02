combat.py --engine-config-file combat.json ^
--engine config-name="Deuterium v2019.2 mobility130" tc=5000+50 --engine config-name="Deuterium v2019.2" tc=5000+50 ^
--opening file="grand_swiss_2019_6plies.epd" random=true ^
--round 8 ^
--reverse ^
--engine-log ^
--log-filename "mylog.txt" ^
--win-adjudication score=700 count=4 ^
--parallel 2

pause