# wordgame

## Data file format

The first line must indicate file format version for compatibility check.

Entries a delimited with an empty line.
The first line of each entry must be a word. Subsequent key-value pairs are optional.

For example:

```
@version 1.0.0

Apfel, der
image: https://uvmbored.com/wp-content/uploads/2017/10/apple-heart-health.png
ex:
- Der Apfel fällt nicht weit vom Stamm.

Woche, die
image: https://www.stjosephswetherby.com/wp-content/uploads/2018/11/d5e43e1b-43dd-4fbb-8779-a74958fffc62-1000x1000.jpg
ex:
- Es sind sieben (7) Tage in jeder Woche.
```
