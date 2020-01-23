$(document).ready(function(){
    (function($){ 
      var cards = $(".card-drop"),
          toggler = cards.find(".toggle"),
          links = cards.find("ul>li>a"),
          li = links.parent('li'),
          count = links.length,
          width = links.outerWidth();
  
  console.info(count);
  console.info(width);
  console.info(toggler);
  console.info(links);
  console.info(li);
  console.info(cards );
  
          //set z-Index of drop Items
          links.parent("li").each(function(i){
              $(this).css("z-index" , count - i); //invert the index values
          });
  
          //set top margins & widths of li elements
          function setClosed(){
              li.each(function(index){
                   $(this).css("top" , index *2)
                                                
                           .css("width" , width - index *20)
                           .css("margin-left" , (index*20)/2)
                                                  .css("margin-left" , (index*20)/2);
              });
                         
              li.addClass('closed');
              toggler.removeClass("active");
          }
          setClosed();
  
      /* -------------------------------------------------------- */ 
      /*	Toggler Click handler
      /* -------------------------------------------------------- */ 
      toggler.on("mousedown" , function(){
          var $this = $(this); //cache $(this)
          //if the menu is active:
                 console.info(this);
          if($this.is(".active")){
              setClosed();
          }else{
              //if the menu is un-active:
              $this.addClass("active");
              li.removeClass('closed');
              //set top margins
              li.each(function(index){
                   $(this).css("top" , 60 * (index + 1))
                           .css("width" ,"70%")
                           .css("margin-left" , "40px");
              });
          }
      });
  
      /* -------------------------------------------------------- */ 
      /*	Links Click handler
      /* -------------------------------------------------------- */ 
      links.on("click" , function(e){
          var $this = $(this),
              label = $this.data("label");
              icon = $this.children("i").attr("class");
              
              li.removeClass('active');
          if($this.parent("li").is("active")){
              $this.parent('li').removeClass("active");
          }else{
              $this.parent("li").addClass("active");
          }
          toggler.children("span").text(label);
          toggler.children("i").removeClass().addClass(icon);
          setClosed();
          e.preventDefault;
          console.log(label);
          d3.select("body").selectAll("svg").remove();
          createGraph();

      });
  
  })(jQuery);
  }); 

function createGraph(){
   /* Diagram */
  var treeData = [
    {
      "name": "Top Level",
      "parent": "null",
      "children": [
        {
          "name": "Level 2: A",
          "parent": "Top Level",
          "children": [
            {
              "name": "Son of A",
              "parent": "Level 2: A"
            },
            {
              "name": "Daughter of A",
              "parent": "Level 2: A"
            }
          ]
        },
        {
          "name": "Level 2: B",
          "parent": "Top Level"
        }
      ]
    }
  ];
  
  
  // ************** Generate the tree diagram	 *****************
  var margin = {top: 5, right: 120, bottom: 20, left: 200},
      width = 960 - margin.right - margin.left,
      height = 700 - margin.top - margin.bottom;
      
  var i = 0,
      duration = 750,
      root;
  /*
  Creates a new tree layout with the default settings: the default sort order is null; 
  the default children accessor assumes each input data is an object with a children array; 
  the default separation function uses one node width for siblings, and two node widths for non-siblings; 
  the default size is 1×1.
  */
  var tree = d3.layout.tree()
      .size([height, width]);
  
  var diagonal = d3.svg.diagonal()
      .projection(function(d) { return [d.y, d.x]; });
  
  var svg = d3.select("#grid")
      .append("svg")
      .attr("id","treeg")
      .attr("width", width + margin.right + margin.left)
      .attr("height", + height + margin.top  + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  root = treeData[0];
  root.x0 = height / 2;
  root.y0 = 0;
    
  update(root);
  /*
  self: if not redefined (typically as copy of this) than it is window object which always points to window. 
  So they can be used interchangeably.
    
  window.frameElement: Returns the element (such as <iframe> or <object>) in which the window is embedded, 
    or null if the window is top-level.
  */
  d3.select(self.frameElement).style("height", "500px");
  
  function update(source) {
  
    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);
  
    // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 180; });
  
    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); });
  
    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", click);
  
    nodeEnter.append("circle")
        .attr("r", 1e-6)
        .style("fill", function(d) { return d._children ? "coral" : "#fff"; });
  
    nodeEnter.append("text")
        .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
        .text(function(d) { return d.name; })
        .style("fill-opacity", 1e-6);
  
    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });
  
    nodeUpdate.select("circle")
        .attr("r", 10)
        .style("fill", function(d) { return d._children ? "coral" : "#fff"; });
  
    nodeUpdate.select("text")
        .style("fill-opacity", 1);
  
    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();
  
    nodeExit.select("circle")
        .attr("r", 1e-6);
  
    nodeExit.select("text")
        .style("fill-opacity", 1e-6);
  
    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function(d) { return d.target.id; });
  
    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function(d) {
          var o = {x: source.x0, y: source.y0};
          return diagonal({source: o, target: o});
        });
  
    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);
  
    // Transition exiting nodes to the parent's new position.
    
    link.exit().transition()
        .duration(duration)
        .attr("d", function(d) {
          var o = {x: source.x, y: source.y};
          return diagonal({source: o, target: o});
        })
        .remove();
  
    // Stash the old positions for transition.
    nodes.forEach(function(d) {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }
  
  // Toggle children on click.
  function click(d) {
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else {
      d.children = d._children;
      d._children = null;
    }
    update(d);
  }


}
 

  