# Guía de contribución

Bienvenido a la guía de contribución, te pedimos que seas respetuoso al momento de colaborar con nosotros.

Puedes iniciar leyendo nuestro [código de conducta](CODE_OF_CONDUCT.md) y [contrato de licencia](LICENSE.md).

## Prerequisitos

Tener instalado node y npm.

## Configuración

Este repositorio hace uso de [Conventional Commits](https://www.conventionalcommits.org/) y cualquier aporte es ideal que haga uso de este. 
Para facilitar el uso de este hemos hecho uso de librerías de node para el manejo de versiones y commits con git hooks. Para habilitarlos ejecuta el siguiente comando:

```bash
npm install
```
Una vez ejecutado este comando estamos listos para empezar la contribución.

## Branches y Commits

Primero que todo es necesario crear una rama `feature/<nombre-de-la-feature> - <id-issue(opcional)>` o `bugfix/<nombre-de-la-bugfix> - <id-issue(opcional)>` y empezar a trabajar en ella.

Al momento de realizar un commit asegurate de hacer uso de las [convenciones](https://www.conventionalcommits.org/) para cada commit, al momento de ejecutar git commit se correran los git hooks para comprobar si efectivamente se utilizaron las convenciones.

### Ejemplo commit erroneo

```bash
$ git commit -a -m "Set up Husky and commitlint"

# Output
⧗   input: Add Husky and commitlint
✖   subject may not be empty [subject-empty]
✖   type may not be empty [type-empty]

✖   found 2 problems, 0 warnings
ⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint

husky - commit-msg hook exited with code 1 (error)
```
### Ejemplo commit correcto:
```bash
$ git commit -m 'feat: set up husky and commitlint'

# Output
[master f1e4dec] feat: set up husky and commitlint
 1 file changed, 26 deletions(-)
 delete mode 100644 XXXXXX.md
```

# Enviar pull request
- Sus cambios propuestos deben ser descritos y discutidos primero en un issue.
- Abra la rama en una fork personal del repositorio, no en el repositorio original.
- Cada pull request debe ser pequeña y representar un solo cambio. Si el problema es complicado, divídalo en múltiples problemas y solicitudes de extracción.

Apreciamos mucho el poder colaborar juntos <3.