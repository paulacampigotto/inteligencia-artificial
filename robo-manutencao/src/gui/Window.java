package gui;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import entity.Cell;
import entity.Robot;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.util.Arrays;
import java.util.Random;
import javax.imageio.ImageIO;

public class Window extends javax.swing.JFrame {

    public Window() {
        initComponents();
        setLocationRelativeTo(null);
        colorMap.put(0, new Color(146, 209, 79));
        colorMap.put(1, new Color(145, 138, 83));
        colorMap.put(2, new Color(83, 142, 212));
        colorMap.put(3, new Color(217, 108, 17));
        toolsMap.put(1, 20);
        toolsMap.put(2, 10);
        toolsMap.put(3, 8);
        toolsMap.put(4, 6);
        toolsMap.put(5, 4);
        colorMap.put(4, Color.black);
        add(grid);
        grid.setVisible(false);
        jMenuItem6.setEnabled(false);
        insertBarrier.setEnabled(false);
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jMenuBar1 = new javax.swing.JMenuBar();
        jMenu1 = new javax.swing.JMenu();
        jMenuItem1 = new javax.swing.JMenuItem();
        jMenu2 = new javax.swing.JMenu();
        disposeTools = new javax.swing.JMenuItem();
        disposeFactories = new javax.swing.JMenuItem();
        disposeRobot = new javax.swing.JMenuItem();
        disposeAll = new javax.swing.JMenuItem();
        insertBarrier = new javax.swing.JMenuItem();
        jMenuItem6 = new javax.swing.JMenuItem();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setResizable(false);

        jMenu1.setText("File");

        jMenuItem1.setText("Open");
        jMenuItem1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem1ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem1);

        jMenuBar1.add(jMenu1);

        jMenu2.setText("Edit");

        disposeTools.setText("Dispose tools");
        disposeTools.setEnabled(false);
        disposeTools.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                disposeToolsActionPerformed(evt);
            }
        });
        jMenu2.add(disposeTools);

        disposeFactories.setText("Dispose factories");
        disposeFactories.setEnabled(false);
        disposeFactories.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                disposeFactoriesActionPerformed(evt);
            }
        });
        jMenu2.add(disposeFactories);

        disposeRobot.setText("Dispose robot");
        disposeRobot.setEnabled(false);
        disposeRobot.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                disposeRobotActionPerformed(evt);
            }
        });
        jMenu2.add(disposeRobot);

        disposeAll.setText("Dispose all");
        disposeAll.setEnabled(false);
        disposeAll.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                disposeAllActionPerformed(evt);
            }
        });
        jMenu2.add(disposeAll);

        insertBarrier.setText("Insert  barrier");
        insertBarrier.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                insertBarrierActionPerformed(evt);
            }
        });
        jMenu2.add(insertBarrier);

        jMenuItem6.setText("Work");
        jMenuItem6.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem6ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem6);

        jMenuBar1.add(jMenu2);

        setJMenuBar(jMenuBar1);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 400, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 279, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void jMenuItem1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem1ActionPerformed
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.showOpenDialog(this);
        try{
            File file = fileChooser.getSelectedFile();
            cells = new ArrayList<>();
            BufferedReader reader = new BufferedReader(new FileReader(file.getAbsolutePath()));
            String strCurrentLine;
            while ((strCurrentLine = reader.readLine()) != null){
                ArrayList<Integer> line = new ArrayList<>();
                String[] temp = strCurrentLine.split(" ");
                for(String i : temp) line.add(Integer.parseInt(i));
                cells.add(line);
            }
            
            
            int cellsNumber = cells.size();
            
            grid.setBounds(0, 0, cellsNumber*CELL_SIZE + 1, cellsNumber*CELL_SIZE + 1 + 40);
            grid.setVisible(true);
            
            setPreferredSize(new Dimension(cellsNumber*CELL_SIZE + getWidth() - getContentPane().getSize().width + 1, 40 + cellsNumber*CELL_SIZE + getHeight() - getContentPane().getSize().height + 1));
            pack();
            
            disposeFactories.setEnabled(true);
            disposeTools.setEnabled(true);
            disposeRobot.setEnabled(true);
            disposeAll.setEnabled(true);
            jMenuItem6.setEnabled(true);
            insertBarrier.setEnabled(true);
        }catch(IOException e){ }
    }//GEN-LAST:event_jMenuItem1ActionPerformed

    private void disposeRobotActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_disposeRobotActionPerformed
        Random rnd = new Random();
        for(int i=0; i<1; i++){
            Cell newRobotCell = new Cell(rnd.nextInt(cells.size()), rnd.nextInt(cells.size()));
            if(!isEmptyCell(newRobotCell)){
                i--;
                continue;
            }
            robotCell = newRobotCell;
        }
        repaint();
    }//GEN-LAST:event_disposeRobotActionPerformed

    private void disposeFactoriesActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_disposeFactoriesActionPerformed
        Random rnd = new Random();
        factoryCells = new ArrayList<>();
        for(int i=0; i<5; i++){
            Cell factoryCell = new Cell(rnd.nextInt(cells.size()), rnd.nextInt(cells.size()));
            if(!isEmptyCell(factoryCell)){
                i--;
                continue;
            }
            factoryCells.add(factoryCell);
        }
        repaint();
    }//GEN-LAST:event_disposeFactoriesActionPerformed

    private HashMap<Integer, Integer> toolsMap = new HashMap<>();
    public final ArrayList<Integer> goals = new ArrayList<>(Arrays.asList(8,5,2,5,2));
    
    private void disposeToolsActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_disposeToolsActionPerformed
        Random rnd = new Random();
        toolCells = new ArrayList<>();
        for(int i=1; i<=5; i++){
            toolCells.add(new ArrayList<>());
            for(int j=0; j<toolsMap.get(i); j++){
                Cell toolCell = new Cell(rnd.nextInt(cells.size()), rnd.nextInt(cells.size()));
                if(!isEmptyCell(toolCell) || !isGreenCell(toolCell)){
                    j--;
                    continue;
                }
                toolCells.get(i-1).add(toolCell);
            }
        }
        repaint();
    }//GEN-LAST:event_disposeToolsActionPerformed

    private void disposeAllActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_disposeAllActionPerformed
        disposeRobotActionPerformed(evt);
        disposeFactoriesActionPerformed(evt);
        disposeToolsActionPerformed(evt);
    }//GEN-LAST:event_disposeAllActionPerformed

    private Robot robot;
    
    private void jMenuItem6ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem6ActionPerformed
        robot = new Robot(this, cells, robotCell, factoryCells, toolCells, new ArrayList<>(Arrays.asList(disposeFactories,
                disposeTools, disposeRobot, disposeAll, jMenuItem6, insertBarrier, jMenuItem1)));
        Thread t = new Thread(robot);
        t.start();
    }//GEN-LAST:event_jMenuItem6ActionPerformed

    private void insertBarrierActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_insertBarrierActionPerformed
        
    }//GEN-LAST:event_insertBarrierActionPerformed

    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Window.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Window.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Window.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Window.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(() -> {
            Window w = new Window();
            w.setVisible(true);
        });
    }
    
    private boolean isEmptyCell(Cell c){
        if(robotCell != null && c.equals(robotCell)) return false;
        if(factoryCells != null)
            for(Cell i : factoryCells)
                if(c.equals(i))
                    return false;
        if(toolCells != null)
            for(ArrayList<Cell> j : toolCells)
                for(Cell i : j)
                    if(c.equals(i))
                        return false;
        return true;
    }
    
    private boolean isGreenCell(Cell c){
        return cells.get(c.x).get(c.y) == 0;
    }
    
    private Cell robotCell = null;
    private ArrayList<Cell> factoryCells = null;
    private ArrayList<ArrayList<Cell>> toolCells = null;
    
    private final int CELL_SIZE = 17;
    private final HashMap<Integer, Color> colorMap = new HashMap<>();
    private final JPanel grid = new JPanel() {
        @Override
        public void paint(Graphics g) {
            super.paint(g);
            Graphics2D gg = (Graphics2D) g.create();
            gg.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            
            int x, y=0;
            for(ArrayList<Integer> i : cells){
                x=0;
                for(int j : i){
                    Rectangle rect = new Rectangle(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE);
                    gg.setColor(colorMap.get(j));
                    gg.fill(rect);
                    gg.setColor(Color.GRAY);
                    gg.draw(rect);
                    x++;
                }
                y++;
            }

            try {
                BufferedImage img;
                int cont = 0;
                if(factoryCells != null)
                    for(Cell i : factoryCells){
                        cont++;
                        if (i == null) continue;
                        img = ImageIO.read(new File("src/gui/factory" + cont + ".png"));
                        gg.drawImage(img, null, i.y*CELL_SIZE, i.x*CELL_SIZE);
                    }
                
                cont = 1;
                if(toolCells != null)
                    for(ArrayList<Cell> j : toolCells){
                        for(Cell i : j){
                            if (i == null) continue;
                            img = ImageIO.read(new File("src/gui/tool" + cont + ".png"));
                            gg.drawImage(img, null, i.y*CELL_SIZE, i.x*CELL_SIZE);
                        }
                        cont++;
                    }
                
                if (robotCell != null){
                    img = ImageIO.read(new File("src/gui/robot.png"));
                    gg.drawImage(img, null, robotCell.y*CELL_SIZE, robotCell.x*CELL_SIZE);
                }
                
                Font f = new Font("TimesRoman", Font.PLAIN, 16);
                gg.setFont(f);
                FontMetrics metrics = gg.getFontMetrics(f);
                
                for(cont=1; cont<=5; cont++){
                    img = ImageIO.read(new File("src/gui/tool" + cont + ".png"));
                    gg.drawImage(img, null, 10 + (cont-1)*(50+CELL_SIZE), grid.getHeight() - 20 - CELL_SIZE/2);
                    gg.drawString(
                            (robot == null ? 0 : goals.get(cont-1) - robot.tools.get(cont-1))
                            + "", 10 + (cont-1)*(50+CELL_SIZE) + CELL_SIZE + 5, grid.getHeight() - 20 + metrics.getAscent()/2);
                }
                
            } catch(IOException e){ }
            
            gg.dispose();
        }
    };
    
    private ArrayList<ArrayList<Integer>> cells;
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JMenuItem disposeAll;
    private javax.swing.JMenuItem disposeFactories;
    private javax.swing.JMenuItem disposeRobot;
    private javax.swing.JMenuItem disposeTools;
    private javax.swing.JMenuItem insertBarrier;
    private javax.swing.JMenu jMenu1;
    private javax.swing.JMenu jMenu2;
    private javax.swing.JMenuBar jMenuBar1;
    private javax.swing.JMenuItem jMenuItem1;
    private javax.swing.JMenuItem jMenuItem6;
    // End of variables declaration//GEN-END:variables
}
