#Draw.io to Vuejs
###A faster way to build web-app by using draw.io as uml to create vue single file components

The most annoying part in creating a web application is to actually create the files and import them in other components. We've solved the problem by using [draw.io](https://www.draw.io) as editor and a little python program to parse the generated UML file and create the file and directory structures.

###Quick Start
Go to [draw.io](https://www.draw.io) create a new file and use the UML objects in order to create your components tree. Be aware, use only the labelled as an **object** (the fist one).
![alt text](https://github.com/FrancescoSaverioZuppichini/drawIoToVuejs/blob/master/images/object.png?raw=true)

You can use arrows to link the components, the relation parent-children is express by having an arrow from the **children** to the **parent**
![alt text](https://github.com/FrancescoSaverioZuppichini/drawIoToVuejs/blob/develop/images/app_drawio_2.png?raw=true)

If you want to also inclued a file into your component you need to use the specific arrow **use**
![alt text](https://github.com/FrancescoSaverioZuppichini/drawIoToVuejs/blob/develop/images/app_drawio_2.1.png?raw=True)

That means that, for example, the file *Home.vue* will import file *User.vue*.

Once you have finished your application you must export it as XML **not compressed**

Then, to create your components, open the terminal and type

```
cd source/
python3 main.py <pathToXmlFile> <destination>
```
After that, directories and components will be created. By following our example:

```
\\after creating all components
.
├── App.vue
├── components
│   ├── Hello.vue
│   ├── Home
│   │   └── Home.vue
│   └── Index
│       ├── Index.vue
│       └── User
│           └── User.vue
```

If we take a look at *Home.vue* for example we can see that all components are loaded correctly

```javascript
import User from './../Index/User/User.vue'
```

By using Vue webtools:

![alt text](https://github.com/FrancescoSaverioZuppichini/drawIoToVuejs/blob/develop/images/vueDevTool_app_drawio_2.1.png?raw=True)

###Pro Tip
You can fast use the *vue-cli* in order to create an app and then use our program to ovveride *App.vue* and the components folder.