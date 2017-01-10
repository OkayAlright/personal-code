from PIL import Image
import numpy as np
import random

class img_gen(object):
    def __init__(self):
        self.IMAGE_WIDTH = 64
        self.IMAGE_HEIGHT = 64

        self.POPULATION_COUNT = 100
        self.GENERATIONS = 15
        self.LIVE_ON = 0.2
        self.MUTATE_RATE = 0.05

        self.population =[]

        self.SOURCE = Image.open("racket_logo.jpg")
        self.RESULT_NAME = "test.jpeg"

    def run(self):
        self.SOURCE = np.array(list(self.SOURCE.convert('L').getdata())).reshape(self.IMAGE_WIDTH,self.IMAGE_HEIGHT)
        print("GOOD START")
        self.generate_pop()
        for i in range(0,self.GENERATIONS +1):
            print("ON GENERATION {} TOP ANSWER {}".format(i,self.eval_fitness(self.population[0])))
            self.sort_population()
            self.cull_pop()
            self.repopulate()
            self.mutate()
        answer = self.population[0]
        answer_img = Image.fromarray(answer)
        answer_img.save(self.RESULT_NAME)

    
    def generate_pop(self):
        for i in range(0,self.POPULATION_COUNT):
            print(len(self.population))
            self.population.append(self.generate_answer())
        
    def generate_answer(self):
        candidate_answer = np.zeros((self.IMAGE_WIDTH,self.IMAGE_HEIGHT),dtype=np.uint8)
        for x in range(0,self.IMAGE_WIDTH):
            for y in range(0,self.IMAGE_HEIGHT):
                candidate_answer[x][y] = random.randint(0,255)
        return candidate_answer

    def eval_fitness(self,candidate):
        diff = 0
        for x in range(0,self.IMAGE_WIDTH):
            for y in range(0,self.IMAGE_HEIGHT):
                if self.SOURCE[x][y] != candidate[x][y]:
                    diff += 1
        return diff

    def sort_population(self):
        self.population = sorted(self.population,key=self.eval_fitness)

    def cull_pop(self):
        self.population =  self.population[0:int(self.POPULATION_COUNT*self.LIVE_ON)+1]

    def mutate(self):
        for cand in self.population:
            if(random.random() < self.MUTATE_RATE):
                self.slice_with_src(cand)

    def slice_with_src(self, cand):
        for x in range(0,self.IMAGE_WIDTH):
            for y in range(0,self.IMAGE_HEIGHT):
                if(random.random() < 0.1):
                    cand[x][y] = self.SOURCE[x][y]

    def repopulate(self):
        while(len(self.population) < self.POPULATION_COUNT):
            new_candidate = self.generate_answer()
            parent1 = self.population[random.randint(0,len(self.population) - 1)]
            parent2 = self.population[random.randint(0,len(self.population) - 1)]
            for x in range(0,self.IMAGE_WIDTH):
                for y in range(0,self.IMAGE_HEIGHT):
                    if(random.randint(0,1) == 0):
                        new_candidate[x][y] = parent1[x][y]
                    else:
                        new_candidate[x][y] = parent2[x][y]
            self.population.append(new_candidate)

t = img_gen()
t.run()
    


    
