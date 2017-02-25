#Draw.io to Vuejs
###A faster way to build web-app by using draw.io as uml to create vue single file components

The most annoying part in creating a web application is to actually create the files and import them in oder components. I've solved the problem by using [draw.io](https://www.draw.io) as editor and a little python program to parse the generated UML file and create the file and directory structures.

###Quick Start
Go to [draw.io](https://www.draw.io) create a new file and use the UML objects in order to create your components tree. Be awere, use only the labeled as **object** (the fist one).
![alt text](/Users/VaeVictis/PycharmProjects/drawIoToVuejs/images/object.png)
You can use arrows to link components, the relation parent-children is express by having an arrow from the **childre** to the **parent**
![alt text](/Users/VaeVictis/PycharmProjects/drawIoToVuejs/images/app_drawio.png)

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
└── components
    ├── Home
    │   ├── Home.vue
    │   ├── Shop
    │   │   └── Shop.vue
    │   ├── ShoppingCart
    │   │   └── ShoppingCart.vue
    │   └── UserProfile
    │       └── UserProfile.vue
    └── Index
        ├── FirstSection
        │   └── FirstSection.vue
        └── Index.vue
```

If we take a look at *Home.vue* for example we can see that all components are loaded correctly

```javascript
import Shop from './Shop/Shop.vue'
import UserProfile from './UserProfile/UserProfile.vue'
import ShoppingCart from './ShoppingCart/ShoppingCart.vue'
```
