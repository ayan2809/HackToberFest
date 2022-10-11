# Directory-Tree-Generator
A Python tool used to generate the subdirectories of a directory.

It features a list of parameters in which you can view the subdirectories.

## Usage
You can use this tool as following:
```
gdTree.py dir [-depth] [-sort_by] [-sort_order] [-display_size] [-display_date] [-dir_first]
```

You can type `gdTree.py -h` to see the parameters and how to use it.

## Example input and output

```
>python gdTree.py c:\\vso
```
will return:

```
c:\\vso
   ├── common
   │   ├── sounds
   │   │   ├── OnNewVersion_0407.ogg
   │   │   ├── OnNewVersion_0409.ogg
   │   │   ├── OnNewVersion_040C.ogg
   │   │   ├── OnNewVersion_0411.ogg
   │   │   ├── OnNewVersion_0419.ogg
   │   │   ├── OnNewVersion_0C0A.ogg
   │   │   ├── OnOperationComplete_0407.ogg
   │   │   ├── OnOperationComplete_0409.ogg
   │   │   ├── OnOperationComplete_040C.ogg
   │   │   ├── OnOperationComplete_0411.ogg
   │   │   ├── OnOperationComplete_0419.ogg
   │   │   ├── OnOperationComplete_0C0A.ogg
   │   │   ├── OnProblemDetected_0407.ogg
   │   │   ├── OnProblemDetected_0409.ogg
   │   │   ├── OnProblemDetected_040C.ogg
   │   │   ├── OnProblemDetected_0411.ogg
   │   │   ├── OnProblemDetected_0419.ogg
   │   │   ├── OnProblemDetected_0C0A.ogg
   │   │   ├── OnQuestion_0407.ogg
   │   │   ├── OnQuestion_0409.ogg
   │   │   ├── OnQuestion_040C.ogg
   │   │   ├── OnQuestion_0411.ogg
   │   │   ├── OnQuestion_0419.ogg
   │   │   ├── OnQuestion_0C0A.ogg
   │   │   ├── OnWritableMediaRequired_0407.ogg
   │   │   ├── OnWritableMediaRequired_0409.ogg
   │   │   ├── OnWritableMediaRequired_040C.ogg
   │   │   ├── OnWritableMediaRequired_0411.ogg
   │   │   ├── OnWritableMediaRequired_0419.ogg
   │   │   └── OnWritableMediaRequired_0C0A.ogg
   │   └── VsoRep
   │       └── vsorep.exe
   └── pcsetup
       └── PcSetup.exe
```

