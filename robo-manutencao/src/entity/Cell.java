package entity;

public class Cell {

    public int x, y;

    public Cell(int x, int y){
        this.x = x;
        this.y = y;
    }
    
    @Override
    public boolean equals(Object o){
        if(o instanceof Cell){
            Cell c = (Cell) o;
            return c.x == x && c.y == y;
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 41 * hash + this.x;
        hash = 41 * hash + this.y;
        return hash;
    }
}
