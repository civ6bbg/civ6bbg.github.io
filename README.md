# civ6bbg.github.io

Site to help users track changes across multiple BBG versions and the Base game.

## Contributing

Install python & install the dependencies:

```bash
pip install -r requirements.txt
```


Create a folder called `sqlFiles` and download the file `CivVILocalization.sqlite`, created by modder Fuzzle:

https://drive.google.com/file/d/1XNd3cxSq5DFMC34Uu4pFQhscx0FF3n9c/view?usp=drivesdk

Download the static versions of the previous versions here:

https://github.com/CivilizationVIBetterBalancedGame/BetterBalancedGame/releases

Go to:

`C:\Users\Your Username\AppData\Local\Firaxis Games\Sid Meier's Civilization VI\Logs`

And copy `DebugGameplay.sqlite` and `DebugConfiguration.sqlite` of that version to `sqlFiles/[VERSION]`.

For base game the file name is `baseGame`.