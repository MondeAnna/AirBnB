<center><h3>AirBnB</h3></center>

A simple, deployable _clone_ of the **AirBnB** website.

<br />
<br />

<center><h4>Front-End</h4></center>

[Landing Page](img/fin-prod.png)

<br />
<br />

<center><h4>Back-End</h4></center>
<center><h5>`Interactive Mode`</h5></center>

```
$ ./console.py
(anna) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(anna) 
```

<br />

<center><h5>`Non-Interactive Mode`</h5></center>

```
$ echo "help" | ./console.py
(anna)

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(anna) 
```

<br />
<br />

<center><h3>Project Execution</h3></center>

<center><h4>Command Line Interface</h4></center>

```
$ ./console.py
(anna)
```

<br />
<br />

<center><h4>CLI Usages by Example</h4></center>

<br />

_**Usage: create <class-name>**_

```
(anna) create State
3aa5babc-efb6-4041-bfe9-3cc9727588f8
(anna)
```

<br />

_**Usage: show <class_name> <_id>**_

```
(anna) show State a94e4705-41e9-4dc3-b492-06eb5792fa00
[State] (a94e4705-41e9-4dc3-b492-06eb5792fa00) {'__class__': 'State', 'updated_at': '2024-05-27T03:39:12.773123', 'id': 'a94e4705-41e9-4dc3-b492-06eb5792fa00', 'created_at': '2024-05-27T03:39:12.773123'}
(anna)  
```

<br />

_**Usage: destroy <class_name> <_id>**_

```
(anna) destroy City 7635272b-27ed-4f6c-bd21-3cad0b6f9e7e
(anna) show City 7635272b-27ed-4f6c-bd21-3cad0b6f9e7e
** no instance found **
(anna)   
```

<br />

_**Usage: update <class_name> <_id>**_

```
(anna) update Place 6fa46404-febe-4618-965f-9f55a862e6b4 first_name = 'pikachu'
(anna) show Place 6fa46404-febe-4618-965f-9f55a862e6b4
[Place] (6fa46404-febe-4618-965f-9f55a862e6b4) {'__class__': 'Place', 'updated_at': '2024-05-27T03:39:12.773257', 'id': '6fa46404-febe-4618-965f-9f55a862e6b4', 'created_at': '2024-05-27T03:39:12.773257', 'first_name': 'pikachu'}
(anna)
```

<br />

_**Usage: all**_

```
(anna) all
Amenity.26c4b6bb-d0df-4628-90d1-53de28757c56
Place.779aba5d-7d5e-496e-882d-16dfa85d8580
User.f94a1ebe-1e81-41c3-a4e0-6b4b84fe8727
(anna)
```

<br />

_**Usage: all <class_name>**_

```
(anna) all User
User.f94a1ebe-1e81-41c3-a4e0-6b4b84fe8727
(anna)
```

_**Usage: <class_name>.all()**_

```
(anna) User.all()
["[User] (b84d6176-35ff-49cc-b881-28d60ed81286) {'__class__': 'User', 'updated_at': '2024-05-27T03:39:12.773284', 'id': 'b84d6176-35ff-49cc-b881-28d60ed81286', 'created_at': '2024-05-27T03:39:12.773284'}", "[User] (ff761ddb-cf6c-424d-a178-27037f64104e) {'__class__': 'User', 'updated_at': '2024-05-27T03:39:12.773399', 'id': 'ff761ddb-cf6c-424d-a178-27037f64104e', 'created_at': '2024-05-27T03:39:12.773399'}"]
```

<br />

_**Usage: <class_name>.destroy(<id>)**_

```
(anna) User.destroy("b84d6176-35ff-49cc-b881-28d60ed81286")
(anna)
(anna) User.all()
["[User] (ff761ddb-cf6c-424d-a178-27037f64104e) {'__class__': 'User', 'updated_at': '2024-05-27T03:39:12.773399', 'id': 'ff761ddb-cf6c-424d-a178-27037f64104e', 'created_at': '2024-05-27T03:39:12.773399'}"]
```

<br />

_**Usage: <class_name>.update(<id>, <attribute-name>, <attribut-value>)**_

```
(anna) User.update("ff761ddb-cf6c-424d-a178-27037f64104e", name, "Kaiju no. 8")
(anna)
(anna) User.all()
["[User] (ff761ddb-cf6c-424d-a178-27037f64104e) {'__class__': 'User', 'updated_at': '2024-05-27T03:39:12.773399', 'id': 'ff761ddb-cf6c-424d-a178-27037f64104e', 'created_at': '2024-05-27T03:39:12.773399', 'name': 'Kaiju No. 8'}"]
```

<br />

_**Usage: <class_name>.update(<id>, <dictionary>)**_

```
(anna) User.update("ff761ddb-cf6c-424d-a178-27037f64104e", {'name': 'Kaiju The Best', 'age': 33})
(anna)
(anna) User.all()
["[User] (ff761ddb-cf6c-424d-a178-27037f64104e) {'__class__': 'User', 'updated_at': '2024-05-27T03:39:12.773399', 'id': 'ff761ddb-cf6c-424d-a178-27037f64104e', 'created_at': '2024-05-27T03:39:12.773399', 'name': 'Kaiju The Best', 'age': 33}"]
```

<br />
<br />

<center><h3>Project Objectives</h3></center>

Create a website capable of:
    * User friendliness
    * A RestfulAPI
    * `Command Line Interface` data manipulation
    * Variadic data storage

<br />
<br />

<center><h4>The Command Line</h4></center>

The developer is provided an interface allowing for the `creation`, `reading`, `updating` and `deletion` of data.

<br />
<br />

<center><h4>Storage</h4></center>

The driving ideology is that the developer is to have ease of use by separating data management from its technical execution. What this then allows is for the data to be managed both from the `cli` as well as any other interface (e.g. `GUI`), all to the same effect.

This abstraction also allows for the storage format to be changed without effect to the code. This in turn means that should the manner in which one wishes to make the data persist becomes a matter of providing the 'plugin' that stores in said format.

<br />
<br />

<center><h4>Test Execution</h4></center>

_**All Tests:**_ `python3 -m unittest discover tests`

_**File Specific:**_ `python3 -m unittest <path-to-file>`

_**Non-Interactive Mode:**_ `echo "python3 -m unittest discover tests" | bash`

<br />
