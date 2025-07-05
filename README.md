# Django Rest Framework

## Basic Requirements

### Python JSON

Python has a built-in package called `json`, which is used to work with JSON data.

- `dumps()`: This is used to convert Python object into JSON string.

**Example:**

```python
import json
python_data = {'name' : 'Abhay', 'roll_no' : 1}
json_data = json.dumps(python_data)
````

* `loads()`: This is used to parse JSON string.

```python
import json
json_data = '{"name" : "Abhay", "roll_no" : 1}'
parsed_data = json.loads(json_data)
```

---

## Serializers / Serialization

In DRF, serializers are responsible for converting complex data types such as querysets and model instances to native Python datatypes (called serialization) that can then be easily rendered into JSON, XML or other content types which is understandable by frontend.

### Serializer

DRF provides a `Serializer` class which gives you a powerful, generic way to control the output of your response, as well as `ModelSerializer` class which provides a useful shortcut for creating serializers that deal with model instances and querysets.

### How to create serializer class

#### Suppose you have a model

```python
class <Model_Name>(models.Model):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
```

Now after these tables are created we want to give this data to frontend so we need to convert this into JSON data — that's when serializer comes into picture.

#### Create a separate `serializers.py`

```python
from rest_framework import serializers

class <Serializer_Name>(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
```

---

### Whole process will look like this:

> **(Step 1)** Complex DataType
> \--(serialization)→
> **(Step 2)** Python Native DataType
> \--(render into JSON)→
> **(Step 3)** JSON Data

The process of converting complex data such as querysets and model instances to native Python datatypes is called **Serialization** in DRF.

---

### In case of one query

* **Step 1:** Creating model instance

```python
<model_instance> = <Model_Name>.objects.get(id=1)
```

* **Step 2:** Converting model instance to Python Dict (Serializing Object)

```python
serializer = <Serializer_Name>(<model_instance>)
```

---

### In case of queryset

* **Step 1:** Creating QuerySet

```python
<model_instance> = <Model_Name>.objects.all()
```

* **Step 2:** Converting queryset to Python Dict (Serializing Object)

```python
serializer = <Serializer_Name>(<model_instance>, many=True)
```

---

## JSONRender

**Step 3:** This is used to render Serialized data into JSON which is understandable by Front End.

```python
from rest_framework.renderers import JSONRenderer

json_data = JSONRenderer().render(serializer.data)
```

---

## JsonResponse

An `HttpResponse` subclass that helps to create a JSON-encoded response. It inherits most behavior from its superclass with a couple of differences:

* Its default `Content-Type` header is set to `application/json`.
* The first parameter, `data`, should be a `dict` instance. If the `safe` parameter is set to `False` it can be any JSON-serializable object.
* The encoder, which defaults to `django.core.serializers.json.DjangoJSONEncoder`, will be used to serialize the data.
* The `safe` boolean parameter defaults to `True`. If it's set to `False`, any object can be passed for serialization (otherwise only dict instances are allowed). If `safe` is `True` and a non-dict object is passed as the first argument, a `TypeError` will be raised.

**When using JsonResponse we can skip this:**

```python
json_data = JSONRenderer().render(serializer.data)
return HttpResponse(json_data)
```

**Instead, directly do:**

```python
return JsonResponse(serializer.data)
```

---

## De-serialization

Deserialization allows parsed data to be converted back into complex types, after first validating the incoming data.

Serializers are also responsible for deserialization, which means they allow parsed data to be converted back into complex types, after first validating the incoming data.

> **Json Data**
> \--(Parsed Data)→
> **Python Native DataType**
> \--(De-serialization)→
> **Complex DataType**

We use `BytesIO` or `JSONParser` to parse JSON data into Python native data types.

```python
from rest_framework.parsers import JSONParser
import io
json_data = b'{"name" : "Abhay", "roll_no" : 1}'
stream = io.BytesIO(json_data)  # json_data is expected to be bytes object
parsed_data = JSONParser().parse(stream)  # Deserialize into Python dict
```

But in modern DRF, `request` object handles this automatically:

* It uses the appropriate parser class (e.g., `JSONParser`) from the `DEFAULT_PARSER_CLASSES` setting.
* Parses `request.body` into Python-native data.
* Makes that data available via `request.data`.
* DRF looks at the `Content-Type` header (e.g., `application/json`).
* Finds the right parser (`JSONParser` by default).
* Parses the body and populates `request.data`.

So when you do:

```python
serializer = <MyModelSerializer>(data=request.data)
```

You're getting already-parsed Python `dict` data — you never touch `JSONParser` or `BytesIO` manually.

---

### Validating and Creating

Now after `parsed_data` (which is automatically handled), we get it in `request.data`:

```python
serializer = <Serializer>(data=request.data)

if serializer.is_valid():  # check the data is in valid format
    serializer.validated_data  # returns parsed and validated data
else:
    serializer.errors
```

---

## Create Data / Insert Data

```python
from rest_framework import serializers

class <Serializer>(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()

    def create(self, validate_data):
        return <Model_Name>.objects.create(**validate_data)
```

### Parital Update Data / Complete Update Data

```python
from rest_framework import serializers

class <SerializerName>(serializers.Serialize):
    first_attribute = serialize.CharField(max_length=255)
    second_attribute = serialize.CharField(max_length=255)
    third_attribute = serialize.CharField(max_length=255)

    def update(self, instance, validated_data): # In this you will see data like this (self, old_data, new_data)
        instance.first_attribute = validated_data.get('first_attribute', intance.first_attribute)
        instance.second_attribute = validated_data.get('second_attribute', intance.second_attribute)
        instance.third_attribute = validated_data.get('third_attribute', intance.third_attribute)
        instance.save()
        return instance
```
By default, serializers must be passed values for all required fields or they will raise validation errors.

- Complete Update Data
Required all data from frontend/client
serializer = StudentSerializer(<instance-name>, data = pythondata)
if serializer.is_valid():
    serializer.save()

- Partial Update Data
serializer = StudentSerializer(<instance-name>, data = pythondata, partial = True)
if serializer.is_valid():
    serializer.save()


### Generics in DRF
Without generics, you'd have to manually handle:

- Getting the model instance
- Serializing the data
- Validating input
- Sending proper HTTP responses
- Handling different request methods
With generics, DRF does that for you.

##### How it works ?
| Class                          | Methods Supported               | Purpose                          |
| ------------------------------ | ------------------------------- | -------------------------------- |
| `ListAPIView`                  | `GET`                           | List all objects                 |
| `CreateAPIView`                | `POST`                          | Create a new object              |
| `RetrieveAPIView`              | `GET`                           | Get a single object by ID        |
| `UpdateAPIView`                | `PUT` / `PATCH`                 | Update an existing object        |
| `DestroyAPIView`               | `DELETE`                        | Delete an object                 |
| `ListCreateAPIView`            | `GET`, `POST`                   | Combine list and create          |
| `RetrieveUpdateDestroyAPIView` | `GET`, `PUT`, `PATCH`, `DELETE` | Combine retrieve, update, delete |
---

## Notes

* `serializer.data`: Using this we can see what is the data inside serializer.


