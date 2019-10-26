package entity;

import java.util.ArrayList;
import java.util.Comparator;
import javafx.util.Pair;

public class Graph {
    private ArrayList<Object> nodes;
    private ArrayList<ArrayList<Pair<Integer, Integer>>> adj = new ArrayList<>();
    
    public Graph(ArrayList<Object> nodes){
        this.nodes = nodes;
        nodes.forEach((_item) -> {
            adj.add(new ArrayList<>());
        });
    }
    
    public void addEdge(Object a, Object b, int distance){
        int a_i = nodes.indexOf(a);
        int b_i = nodes.indexOf(b);
        adj.get(a_i).add(new Pair(b_i, distance));
    }
    
    private double A_star_distance(int a, Pair<Integer, Integer> b, ArrayList<Object> finalNodes){
        double res = b.getValue();
        if(finalNodes.size() > 1)
            return res;
        Cell ca = (Cell) nodes.get(a);
        Cell cb = (Cell) nodes.get(b.getKey());
        Cell cc = (Cell) finalNodes.get(0);
        return res - Math.sqrt(Math.pow(ca.x - cc.x, 2) + Math.pow(ca.y - cc.y, 2)) +
                Math.sqrt(Math.pow(cb.x - cc.x, 2) + Math.pow(cb.y - cc.y, 2));
    }
    
    public ArrayList<Object> A_star(Object initialNode, ArrayList<Object> finalNodes){
        ArrayList<Double> distances = new ArrayList<>();
        nodes.forEach((_item) -> {
            distances.add(Double.MAX_VALUE);
        });
        
        ArrayList<Integer> prev = new ArrayList<>();
        nodes.forEach((_item) -> {
            prev.add(-1);
        });
        
        ArrayList<Integer> finalNodesIndexes = new ArrayList<>();
        finalNodes.forEach((node) -> {
            finalNodesIndexes.add(nodes.indexOf(node));
        });
        
        ArrayList<Pair<Integer, Double>> stack = new ArrayList<>();
        distances.set(nodes.indexOf(initialNode), 0.0);
        stack.add(new Pair<>(nodes.indexOf(initialNode), 0.0));
        
        int finalNodeIndex = -1;
        
        Comparator<Pair<Integer, Double>> sortComp = new Comparator<Pair<Integer, Double>>() {
            @Override
            public int compare(Pair<Integer, Double> p1, Pair<Integer, Double> p2) {
                return p1.getValue().compareTo(p2.getValue());
            }
        };
        
        while(!stack.isEmpty()){
            
            Pair<Integer, Double> top = stack.remove(0);
            
            for(int node : finalNodesIndexes)
                if(node == top.getKey()){
                    finalNodeIndex = node;
                    break;
                }
            
            if(finalNodeIndex != -1) break;
            
            for(Pair<Integer, Integer> node : adj.get(top.getKey())){
                double temp = top.getValue() + A_star_distance(top.getKey(), node, finalNodes);
                if(temp < distances.get(node.getKey())){
                    stack.add(new Pair(node.getKey(), temp));
                    prev.set(node.getKey(), top.getKey());
                    distances.set(node.getKey(), temp);
                }
            }
            
            stack.sort(sortComp);
            
        }
        
        ArrayList<Object> path = new ArrayList<>();
        
        while(finalNodeIndex != -1){
            path.add(0, nodes.get(finalNodeIndex));
            finalNodeIndex = prev.get(finalNodeIndex);
        }
        
        return path;
    }
    
    /*public static void main(String[] args){
        ArrayList<Object> nodes = new ArrayList<>();
        nodes.add("a");
        nodes.add("b");
        nodes.add("c");
        nodes.add("d");
        nodes.add("e");
        Graph g = new Graph(nodes);
        g.addEdge("a", "b", 5);
        g.addEdge("b", "e", 7);
        g.addEdge("b", "c", 2);
        g.addEdge("c", "d", 3);
        g.addEdge("d", "e", 1);
        ArrayList<Object> finalNode = new ArrayList<>();
        finalNode.add("e");
        ArrayList<Object> path = g.dijkstra("a", finalNode);
        for(Object i : path)
            System.out.println(i);
    }*/
}
