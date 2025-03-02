# Introduction

OpenScatter is a free and open-source Blender addon for advanced scattering. It's built from the ground up with artists in mind. It includes various features to simulate the natural patterns of foliage growth, as well as less realistic features for users who want artistic control. 
Key Benefits: 

- Control: Fine-tune density, scale, rotation, and dynamic behavior.
- Realism: Various advanced features to create realistic scatter systems.
- Performance: Advanced optimization features for viewport and render efficiency.

# Installation

1. Open Blender and go to Edit -> Preferences -> Add-ons. 
2. Press the arrow button in the top-right corner and hit "Install from Disk".
3. Locate where you saved the addon, select it and hit "Install from Disk". 

Done!

# Basic Setup

**Accessing OpenScatter:**

Once installed, open the N-Panel/Sidebar, and you'll find the addon panel in the OpenScatter category. 

**Initial Configuration:**

When you've located the addon panel, you can simply choose an emitter and then click the '+' icon to add a new scatter system. From here you can choose the desired surface, the instances you want to scatter and so on. 

# Scattering System Overview

OpenScatter works with what is called "Scatter Systems". In the top of the addon panel you'll find a list which contains all the scatter systems in the scene. 

Each scatter system can be thought of as a layer of it's own. For example, if you're working on a nature scene, you could have one layer for grass, one for some leaves, one for some clover, and so on. Each "layer" has its own settings and properties. This system makes it easy to keep everything organized and easy to work with. 

# Basic Scattering

To scatter objects on a surface you first need to have an emitter selected. Then, click the '+' icon in the top-right of the addon panel. This will add a new scatter system using the selected emitter object. 

Now, go to the "Instances" category. Here you can choose which instances to scatter on the surface. You can use the 'Type' menu to switch between scattering a single object and a collection. 
To control your scattering, go to the "Scattering" category. Here you can control the density and seed. You can also enable the option called "Limit Self-Collision". This will show you a new value that you can change. This will control the minimum distance between each scattered object. 
From here, you can play around with all the different categories to get the results you want. We'll go into details on each of these on the following pages.

# Surfaces

The way OpenScatter works is by allowing you to choose an emitter object as the surface. When you've selected a surface you can add scatter system to it. All scatter systems will be using the emitter object that you have selected when you add a new scatter system. You can also choose custom surfaces for each individual scatter system. This can be useful in some instances, but it often makes more sense to use the emitter object. 

Using the emitter object, allows OpenScatter to keep track of all the scatter systems and where they belong. For example, you can have one surface where you have some scatter systems. Now if you choose another surface as the emitter object, the other scatter systems will still remain, but you'll be able to create and edit scatter sytems on the new emitter object. This way you can easily switch between different emitter objects. 

If you need it, you can also choose to use multiple surfaces. You do this by creating a collection containing your surfaces and then selecting that collection in the addon panel. 

# Instance Options

Choosing instances is very similar to choosing surfaces. You have a 'Type' menu where you choose to use a single instance or a collection of instances. Using a collection of instances can be very useful if you want variety. For example, you can have a collection of variations of a grass clump. Scattering different variations can give you a much more natural look.

# Scattering Parameters

**Density:**<br>
Control the number of instances per unit area.

**Seed:**<br>
Random seed for generating varied scattering layouts.

**Limit Self-Collision:**<br>
Enable this to prevent instances from overlapping or colliding with each other.

# Scale & Rotation

- ### Scale Options:
  
  - **Uniform Scale:** <br> 
    Keep scaling consistent in all axes.
  
  - **Non-Uniform Scale:** <br> 
    Independently adjust scale per axis.
  
  - **Random Scale:** <br> 
    Introduce randomness into the scaling values.

- ### Rotation Options:
  
  - **Rotate:**<br> 
    Manually set rotation.
  
  - **Align to Surface:**<br>
    Automatically rotate instances to match the surface normal.
  
  - **Random Rotation:**<br>
    Add randomization to the rotation values.

# Culling

**Vertex Group:** <br>
Use a chosen vertex group to control the position of instances.

**Using Vertex Groups on Multiple Objects:** <br>
Using vertex groups when you're using a collection as the surface input can be a bit confusing at first. The way this system works is by using a shared vertex group. Two different objects in your scene can have vertex groups with the same name. When you do this, you have a shared vertex group. Now, select one of the objects with the vertex group, and choose it in the addon panel. Now the vertex groups on both objects will be used as a culling mask in the scatter system.

# Abiotic

The [Abiotic components](https://en.wikipedia.org/wiki/Abiotic_component) in nature are non-living factors like slope, elevation, sunlight angle, temperature, water, air, and soil, which influence how living things survive and grow.

To achieve more realistic results, **OpenScatter** has incorporated the "Slope," "Elevation," and "Angle" masks to control the distribution of your instances.

- **Slope**:  
  The Slope Mask can be used to control the maximum slope that the instances can grow on. For example, trees rarely grow on steep surfaces, so using the feature can be super useful if you're creating something like a mountain with trees on it.

- **Elevation**:  
  The '[Tree Line](https://en.wikipedia.org/wiki/Tree_line)' defines the edge of where trees are no longer able to grow. This often happens at high elevations. Using the elevation mask in **OpenScatter**, you can achieve the same effect. It simply allows you to choose a maximum elevation that the instances can grow to.

- **Angle**:  
  Many plants are affected by sunlight. Using the angle mask can ensure that plants only grow in or out of sunlight to achieve a similar effect to what happens in nature.

# Proximity

The **Proximity** panel allows you to control where instances appear (or don’t appear) based on their distance to specified geometry or curves. You can configure whether instances cluster around (Seek) or avoid (Avoid) those references, with additional settings to fine-tune how quickly the effect fades in or out

### **Geometry Proximity**

**Single / Multiple Objects:**<br>
Choose whether to use a single object or a collection as a reference for proximity calculations.

**Single Object:** <br>
Allows you to pick one specific object.

**Multiple Objecst:** <br>
Lets you select multiple objects (e.g., a collection of rocks, buildings, etc.).

**Object:**<br>
Specify the object (or objects) you want to measure distance from. Instances will be placed (or removed) depending on the proximity to this reference.

**Distance:**<br>
Defines the distance threshold for proximity.
Higher values mean the proximity effect extends farther from the chosen object(s).

**Smooth Transition:**<br>
Enable this to control the transition of the growth. Use the "Transition" value below, to define the smoothness of the transition. 

- **Avoid / Seek**
  
  - Avoid: <br>
    Instances will be sparse or absent near the object within the specified distance.
  
  - Seek: <br>
    Instances will concentrate near the object, within the specified distance.

### **Curve Proximity**

**Single / Multiple Curves:**<br>
Similar to the geometry option, but uses curve objects as the reference.

**Single Curve:** <br>
Use one curve to define your proximity.

**Multiple Curves:** <br>
Use a collection of curves for more complex proximity control.

**Curve:**<br>
Select the specific curve(s) that will influence scattering distribution.

**Distance:**<br>
The proximity range around the curve(s). Instances within this distance (Seek) or beyond this distance (Avoid) are affected.

**Smooth Transition:**<br>
Enable this to control the transition of the growth. Use the "Transition" value below, to define the smoothness of the transition. 

**Infinite Z:**<br>
When enabled, the proximity effect will take effect regardless of the curves position on the vertical axis. 

**Avoid / Seek:**

- Avoid: <br>
  Instances will be sparse or absent near the curve within the specified distance.

- Seek: <br>
  Instances will concentrate near the curve, within the specified distance.

# Ecosystem

The 'Ecosystem' is very similar to the Proximity options. However, the ecosystem works integrated with other scatter systems. This can be super useful when you have a lot of scattering layers and you don't want them to overlap. For example, if you're creating a forest biome, you don't want foliage to grow inside the trees, or sometimes even near them. By using the ecosystem you can make sure that your foliage keeps a certain distance from the trees. Alternatively you can also use attraction to make certain things grow near others. Repulsion pushes away. Attraction, well, attracts. 

# Texture Masks

You can use the 'Texture Masks' feature to control the distribution of objects. The currently supported textures are as follows:

- **Noise** - Creates a semi-randomized and varied look. Great for realistic natural results.
- **Lines** - Creates rows in your scatter system. Could be useful for creating the classic [dutch tulips](https://en.wikipedia.org/wiki/Tulip#Flowers).
- **Tiles** - Creates a grid of tiles. Used for more artistic or [architectural purposes](https://www.pinterest.com/pin/synthetic-turf-and-inset-pavers-the-new-trend-in-landscaping--25473554120437702/).
- **Image** - Use a custom image as the texture mask. 

Changing the falloff values of textures can also create some interesting results as you can practically make it only affect the scale of the objects.
For example, using the noise texture masks, and tuning the falloff can give you natural scale variation that isn't just random, compared to the random scale feature.

# Dynamics

The '**Dynamics**' category contains the '**Wind**' and '**Collision**' features. 

**Wind:**<br>
The wind feature uses procedural noise to control the rotation of your scattered objects. This creates a natural flowy look. A simple yet super useful and convincing solution for creating blowing grass or similar. 

**Collision:**<br>
The collision feature simulates how something like grass might react to an object rolling into it. It will essentially rotate the objects in the direction of the surface normal of the selected object. This creates the effect that an object is pushing down the objects as it's colliding with them. 

# Optimization

The optimization category contains some very useful features for optimizing your scatter systems without sacrificing quality. 

**Decrease Viewport Density:**<br>
This feature will decrease the density in the viewport down to the selected percentage. It will keep it fast in the viewport, and show the original high density in renders. 

**Use Optimized Mesh:**<br>
This feature allows you to use an optimized mesh in the viewport. The current options are:
- Convex Hull - Creates a convex hull around your instances. This is the least optimized version.
- Bounding Box - Creates a bounding box around your instances. Greatly reduces vertex count but also reduces visibility.
- Proxy Object - Using the proxy object option you can choose a premade mesh to represent your instances. It comes with options for things like grass, rocks, trees, etc.

**Camera Culling:**<br>
Using Camera Culling, only objects in the view of the active camera will be rendered. This significantly decrease the amount of instances, without you having to do it manually with something like vertex groups. 

# Working with multiple scenes

If your blend file has several scenes, working with OpenScatter can become a bit more complicated. 

By default, you can create scatter systems in multiple scenes, but since the scatter systems are linked between scenes, the visibility of scatter systems aren't updated between scenes. 

To solve this, I added a refresh button next to the system list. When this is pressed, it will update the visibility of all the scatter systems to match the active scene. When switching to a new scene, you'll have to press it again. 