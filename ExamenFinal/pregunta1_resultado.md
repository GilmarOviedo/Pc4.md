
 +--------------------+       +---------------------+
 |    Notebook        |       |      EventSystem    |
 +--------------------+       +---------------------+
 | - cells: list      |       | - event_queue: deque|
 | - state: dict      |       | - lock: Lock        |
 +--------------------+       | - notebook: Notebook|
 | + execute_cell()   |       +---------------------+
 +--------------------+       | + add_event()       |
                              | + handle_event()    |
                              | + event_loop()      |
                              +---------------------+

          (1)                                      
      Add Event                                   
          +                                       
          |                                       
          v                                       
 +--------------------+                           
 |  EventQueue        |                           
 |                    |                           
 | - "execute Cell 1" |                           
 | - "execute Cell 2" |                           
 | - "execute Cell 3" |                           
 +--------------------+                           
          |                                       
          v                                       
       Dequeue Event                             
          +                                       
          |                                       
          v                                       
 +-------------------+   (2) Execution Order      
 |   execute_cell()  |                           
 | - "Cell 2"        |                           
 | - "Cell 1"        |                           
 | - "Cell 3"        |                           
 +-------------------+                           
