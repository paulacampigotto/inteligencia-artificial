package entity;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JMenuItem;

public class Robot implements Runnable {
    private final int RADAR_RADIUS = 4;
    private final int gridSize;
    private final Cell robotCell;
    private final ArrayList<Cell> factoryCells;
    private final ArrayList<ArrayList<Cell>> toolCells;
    private final JFrame frame;
    private final ArrayList<ArrayList<Integer>> cells;
    private int lastMove;
    public final ArrayList<Integer> tools = new ArrayList<>(Arrays.asList(8,5,2,5,2));
    private final HashMap<Integer, Integer> cellWeights = new HashMap<>();
    private final ArrayList<JMenuItem> buttons;
    
    public Robot(JFrame frame, ArrayList<ArrayList<Integer>> cells, Cell robotCell, ArrayList<Cell> factoryCells, ArrayList<ArrayList<Cell>> toolCells, ArrayList<JMenuItem> buttons){
        this.frame = frame;
        this.cells = cells;
        gridSize = cells.size();
        this.robotCell = robotCell;
        this.factoryCells = factoryCells;
        this.toolCells = toolCells;
        this.buttons = buttons;
        cellWeights.put(0, 1);
        cellWeights.put(1, 5);
        cellWeights.put(2, 10);
        cellWeights.put(3, 15);
        cellWeights.put(4, Integer.MAX_VALUE);
        lastMove = (new Random()).nextInt(4);
        constructGraph();
    }
    
    private ArrayList<Object> searchToolCells(){
        ArrayList<Object> cells = new ArrayList<>();
        for(int i=robotCell.x - RADAR_RADIUS; i<robotCell.x + RADAR_RADIUS; i++)
            for(int j=robotCell.y - RADAR_RADIUS; j<robotCell.y + RADAR_RADIUS; j++){
                if(j<0 || i<0 || j>=gridSize || i>=gridSize)
                    continue;
                for(ArrayList<Cell> k : toolCells)
                    for(Cell l : k)
                        if(l != null && l.x == i && l.y == j)
                            cells.add(l);
            }
        return cells;
    }
    
    private Graph graph;
    
    private void constructGraph(){
        ArrayList<Object> nodes = new ArrayList<>();
        
        for(int i=0; i<cells.size(); i++)
            for(int j=0; j<cells.size(); j++)
                nodes.add(new Cell(i, j));
        
        graph = new Graph(nodes);
        
        for(int i=0; i<cells.size(); i++)
            for(int j=0; j<cells.size(); j++)
                for(int x=i-1; x<=i+1; x++)
                    for(int y=j-1; y<=j+1; y++){
                        if((x!=i && y!=j) || x<0 || y<0 || x>=gridSize || y>=gridSize)
                            continue;
                        graph.addEdge(new Cell(i, j), new Cell(x, y), cellWeights.get(cells.get(x).get(y)));
                    }
    }
    
    private double distance(Cell a, Cell b){
        return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
    }
    
    private ArrayList<Object> A_star(ArrayList<Object> c){
        if(c.size() == 1){
            double minDist = Double.MAX_VALUE;
            Cell minDist_cell = null;
            for(int i=robotCell.x - RADAR_RADIUS; i<=robotCell.x + RADAR_RADIUS; i++)
                for(int j=robotCell.y - RADAR_RADIUS; j<=robotCell.y + RADAR_RADIUS; j++){
                    if(j<0 || i<0 || j>=gridSize || i>=gridSize)
                        continue;
                    Cell temp = new Cell(i, j);
                    double temp1 = distance((Cell)c.get(0), temp);
                    if(temp1 < minDist){
                        minDist = temp1;
                        minDist_cell = temp;
                    }
                }
            c.clear();
            c.add(minDist_cell);
        }
        
        return graph.A_star(robotCell, c);
    }
    
    private void paintAndWait(){
        frame.repaint();
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {}
    }
    
    private int factoryToGo = -1;
    
    @Override
    public void run(){
        for(JMenuItem i : buttons)
            i.setEnabled(false);
        
        int needyFactories = 5;
        while(needyFactories > 0){
            ArrayList<Object> path = null;
            
            ArrayList<Object> tc = searchToolCells();
            
            if(factoryToGo == -1 || tc.size() > 0){
                for(ArrayList<Cell> k : toolCells)
                    if(k.contains(robotCell)){
                        int temp = toolCells.indexOf(k);
                        tools.set(temp, tools.get(temp)-1);
                        if(tools.get(temp) == 0){
                            factoryToGo = temp;
                        }
                        k.set(k.indexOf(robotCell), null);
                    }

                if(tc.isEmpty()){
                    Random rnd = new Random();
                    int randInt = rnd.nextInt(10) + 1;
                    if(randInt == 1)
                        lastMove = (lastMove + 2) % 4;
                    else if(randInt <= 3) lastMove = (lastMove + 1) % 4;
                    else if(randInt <= 5) lastMove = (lastMove + 3) % 4;
                    ArrayList<Object> finalCells = new ArrayList<>();
                    if(lastMove == 0 || lastMove == 2)
                        for(int i=robotCell.x - RADAR_RADIUS; i<=robotCell.x + RADAR_RADIUS; i++){
                            finalCells.add(new Cell(i, robotCell.y + 
                                    (lastMove == 0 ? -1*RADAR_RADIUS : RADAR_RADIUS)
                                ));
                        }
                    else
                        for(int i=robotCell.y - RADAR_RADIUS; i<=robotCell.y + RADAR_RADIUS; i++){
                            finalCells.add(new Cell(robotCell.x + 
                                    (lastMove == 1 ? -1*RADAR_RADIUS : RADAR_RADIUS)
                                , i));
                        }
                    path = A_star(finalCells);
                }else{
                    path = A_star(tc);
                }
            }
            
            if(factoryToGo != -1){
                if(factoryCells.get(factoryToGo).equals(robotCell)){
                    factoryCells.set(factoryToGo, null);
                    factoryToGo = -1;
                    needyFactories--;
                    continue;
                }
                
                ArrayList<Object> finalNode = new ArrayList<>();
                finalNode.add(factoryCells.get(factoryToGo));
                path = A_star(finalNode);
            }
            
            for(Object i : path){
                robotCell.x = ((Cell) i).x;
                robotCell.y = ((Cell) i).y;
                paintAndWait();
            }
         }
        
        for(JMenuItem i : buttons)
            i.setEnabled(true);
    }
}
