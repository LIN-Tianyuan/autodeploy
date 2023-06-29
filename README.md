# Auto deploy
## Main steps

1. git clone https://github.com/LIN-Tianyuan/autodeploy.git
2. cd autodeploy
3. pip install -r requirements.txt
4. python -m autodeploy.main --repo \<The git link of the deployed project> --host \<Remote server name>

## Example

```bash
git clone https://github.com/LIN-Tianyuan/autodeploy.git

cd autodeploy

pip install -r requirements.txt

python -m autodeploy.main --repo https://sgithub.fr.world.socgen/tianyuan-lin/helloworldtest.git --host SRVCLDMBTD006
```

## Project deployed structure example
    
    helloworldtest
    ├── helloworldtest                   # Project main directory
        ├── __init__.py
        ├── main.py                      # Main program
    ├── pyproject.toml                   # Toml file(Fill in the corresponding information [path, dependency] etc...)
    ├── requirements.txt                 # Requirements files

## Contributing
LIN Tianyuan

## License
[MIT](https://choosealicense.com/licenses/mit/)