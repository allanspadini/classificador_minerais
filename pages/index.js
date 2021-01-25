import styled from 'styled-components'
import db from '../db.json';
import Widget from '../src/components/Widget'
import AppBackground from '../src/components/AppBackground'
import GitHubCorner from '../src/components/GitHubCorner'



export const QuizContainer = styled.div`
  width: 100%;
  max-width: 350px;
  padding-top: 45px;
  margin: auto 10%;
  @media screen and (max-width: 500px) {
    margin: auto;
    padding: 15px;
  }
`;

export default function Home() {
  return (
    <AppBackground backgroundImage={db.bg}>
    
      <QuizContainer>
        <Widget>
          <Widget.Content>
            <Widget.Header>
              <h1>Classificador de minerais</h1>


            </Widget.Header>
            

            <p>Suba seu arquivo aqui!</p>

          </Widget.Content>

          
        </Widget>

        <Widget>
          <Widget.Content>
            <h1>Resultado</h1>


          </Widget.Content>
        


        </Widget>

      </QuizContainer>

      <GitHubCorner projectUrl="https://github.com/omariosouto"/>

    
    </AppBackground>
  
  
          
    
    
  )
}
